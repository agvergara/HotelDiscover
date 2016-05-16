from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from models import Hotel, Image, Comment, Config, Favourite
from django.contrib.auth.models import User
from django.template.loader import get_template, render_to_string
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from loaddata import loadhotels
from django.db.models import Count
# Create your views here.

#Functions to return some lists
def orderbycomments():
	#Ordered by the number of comments
	hotel_list = []
	user_list = []
	comments = Hotel.objects.annotate(quantity=Count('comment')).order_by('-quantity')
	if comments[0].quantity > 0:
		for count in range(10):
			if comments[count].quantity > 0:
				hotel = Hotel.objects.get(name=comments[count])
				image = Image.objects.get(hotel=hotel)
				url = image.url_image.split(" ")[0]
				hotel_list += [(hotel, url)]
	#Load user pages
	users = User.objects.all()
	for user in users:
		config = Config.objects.get(user=user)
		user_list += [(user, config.title)]
	return (hotel_list, user_list)

def favourites (user, minpage, maxpage):
	hotel_list = []
	count = minpage
	user = User.objects.get(username=user)
	favourites = Favourite.objects.all()
	for fav in favourites:
		if fav.user == user:
			if count < maxpage:
				image = Image.objects.get(hotel=fav.hotel)
				url = image.url_image.split(" ")[0]
				hotel_list += [(fav.hotel, url, fav.date)]
			else:
				count += 1
	return (hotel_list, user)

# REAL VIEWS.PY

# MAINNNNNNNNNNNNN
def index(request):
	hotel_list = []
	user_list = []
	xml_language = {'spanish' : 'es', 'english' : 'en', 'french' : 'fr'}
	index = 'spanish'
	url = 'http://www.esmadrid.com/opendata/alojamientos_v1_' + xml_language[index] + '.xml'
	hotels = Hotel.objects.all()
	if not hotels:
		loadhotels(url)
	(hotel_list, user_list) = orderbycomments()
	#Getting templates
	template = get_template('index.html')
	context = RequestContext(request, {'hotels' : hotel_list, 'users' : user_list})
	return HttpResponse(template.render(context))

# Page of an user
def userpage(request, user):
	hotel_list = []
	try:
		(hotel_list, user) = favourites(user, 0, 10)
	except ObjectDoesNotExist:
		return HttpResponse(user + " does not exist")
	context = RequestContext(request, {'hotels' : hotel_list})
	template = get_template('userfavs.html')
	return HttpResponse(template.render(context))

"""def usernextpage(request, user, page):
	maxpage = 10 * page
	minpage = maxpage - 9
	hotel_list = []
	try:
		hotel_list = favourites(user, minpage, maxpage)
	except ObjectDoesNotExist:
		return HttpResponse("La has cagao")
	template = get_template('userfavs.html')
	context = RequestContext(request, {'hotels' : hotel_list})
	return HttpResponse(template.render(context))"""

# All of the hotels!
def hotellist(request):
	hotel_list = []
	hotels = Hotel.objects.all()
	for hotel in hotels:
		hotel_list += [(hotel.name, hotel.id)]
	template = get_template('hotellist.html')
	context = RequestContext(request, {'hotel_list' : hotel_list})
	return HttpResponse(template.render(context))

# Page of a single hotel
def hotel(request, identifier):
	img_list = []
	comment_list = []
	hotel = Hotel.objects.get(id=identifier)
	images = Image.objects.get(hotel=hotel)
	for count in range(5):
		try:
			img_list += [images.url_image.split(" ")[count]]
		except IndexError:
			pass
	comments = Comment.objects.all()
	for comment in comments:
		if comment.hotel == hotel:
			comment_list += [comment]
	template = get_template('hotel_id.html')
	context = RequestContext(request, {'hotel' : hotel, 'img_list' : img_list, 'comments' : comment_list})
	return HttpResponse(template.render(context))

#XML channel of an user
def userxml (request, user):
	fav_list = []
	img_list = []
	hotel_list = []
	try:
		user = User.objects.get(username=user)
	except ObjectDoesNotExist:
		return HttpResponse("Does not exists")
	favs = Favourite.objects.all()
	for fav in favs:
		if fav.user == user:
			image = Image.objects.get(hotel=fav.hotel)
			img_list += image.url_image.split(" ")
			fav_list += [fav]
	template = get_template('xml/user_xml.xml')
	context = RequestContext(request, {'hotels' : fav_list, 'imgs' : img_list})
	return HttpResponse(template.render(context), content_type="text/xml")

#Config section!
def saveconf(request):
	user = request.user.username
	color = request.POST.get('color')
	size = request.POST.get('size')
	if request.POST.get('title') is not None:
		title = strip_tags(request.POST.get('title'))
	else:
		title = "Pagina de " + user
	user = User.objects.get(username=user)
	config = Config.objects.get(user=user)
	config.color = color
	config.size = size
	config.title = title
	config.save()
	return HttpResponseRedirect("/")

#Comment section!
def addcomment(request):
	user = request.user.username
	user = User.objects.get(username=user)
	identifier = request.POST.get('identifier')
	hotel = Hotel.objects.get(id=identifier)
	title = strip_tags(request.POST.get('title'))
	comment = strip_tags(request.POST.get('comment'))
	savecomm = Comment(user=user, hotel=hotel, title=title, comment=comment)
	savecomm.save()
	return HttpResponseRedirect("/alojamientos/"+str(identifier))

#Add to the favs!
def addfav (request):
	identifier = request.POST.get('identifier')
	user = request.user.username
	hotel = Hotel.objects.get(id=identifier)
	user = User.objects.get(username=user)
	favourite = Favourite(user=user, hotel=hotel)
	favourite.save()
	return HttpResponseRedirect("/alojamientos/"+str(hotel.id))

# OPTIONAL HERE!
# Main page xml channel
def mainxml (request):
	hotel_list = []
	user_list = []
	ip = "http://" + request.get_host()
	(hotel_list, user_list) = orderbycomments()
	template = get_template('xml/main_xml.xml')
	context = RequestContext(request, {'hotels' : hotel_list, 'users' : user_list, 'ip' : ip})
	return HttpResponse(template.render(context), content_type="text/xml")

# REGISTER!
def register(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	return HttpResponseRedirect('/')