from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from models import Hotel, Image, Comment, Config, Favourite
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login
from loaddata import loadhotels, orderbycomments, orderbycategory, favourites, manypages
from django.db.models import Count
import math
# Create your views here.

#Functions to return some lists

def getlanguage(language, name):
	if language == 'English':
		url = 'http://cursosweb.github.io/etc/alojamientos_en.xml'
	elif language == 'French':
		url = 'http://cursosweb.github.io/etc/alojamientos_fr.xml'
	body = loadhotels(url, True, name)
	return body

# REAL VIEWS.PY

# MAINNNNNNNNNNNNN
def index(request):
	hotel_list = []
	user_list = []
	url = 'http://cursosweb.github.io/etc/alojamientos_es.xml'
	hotels = Hotel.objects.all()
	if not hotels:
		loadhotels(url, False, "")
	(hotel_list, user_list) = orderbycomments()
	#Getting templates
	template = get_template('index.html')
	context = RequestContext(request, {'hotels' : hotel_list, 'users' : user_list})
	return HttpResponse(template.render(context))

# Page of an user
def userpage(request, username):
	hotel_list = []
	num_list = []
	try:
		(hotel_list, user) = favourites(username, 0, 10)
	except ObjectDoesNotExist:
		return HttpResponse(username + " does not exist")
	usr = User.objects.get(username=username)
	(num_list, num_favs) = manypages(usr)
	context = RequestContext(request, {'hotels' : hotel_list, 'username' : username,
										'num_favs' : num_favs, 'max_pg' : num_list})
	template = get_template('userfavs.html')
	return HttpResponse(template.render(context))

def usernextpage(request, username, page):
	maxpage = 10 * int(page)
	minpage = maxpage - 10
	hotel_list = []
	num_list = []
	if page == "1":
		return HttpResponseRedirect("/" + username)
	try:
		(hotel_list, user) = favourites(username, minpage, maxpage)
	except ObjectDoesNotExist:
		return HttpResponse("La has cagao")
	usr = User.objects.get(username=username)
	(num_list, num_favs) = manypages(usr)
	template = get_template('userfavs.html')
	context = RequestContext(request, {'hotels' : hotel_list, 'username' : username,
										'num_favs' : num_favs, 'max_pg' : num_list})
	return HttpResponse(template.render(context))

# All of the hotels!
def hotellist(request):
	hotel_list = []
	categoryflag = False
	starsflag = False
	stars = ""
	category = ""
	#Test if search by category or stars
	try:
		categoryflag = bool(request.POST.get('category').split('=')[1])
	except IndexError:
		category = request.POST.get('category')
	except AttributeError:
		pass
	try:
		starsflag = bool(request.POST.get('stars').split('=')[1])
	except IndexError:
		stars = request.POST.get('stars')
	except AttributeError:
		pass
	if  stars == "" and category == "":
		categoryflag = True
		starsflag = True
	hotel_list = orderbycategory(request, categoryflag, category, starsflag, stars)
	template = get_template('hotellist.html')
	context = RequestContext(request, {'hotel_list' : hotel_list})
	return HttpResponse(template.render(context))

# Page of a single hotel
def hotel(request, identifier):
	img_list = []
	comment_list = []
	language = ""
	hotel = Hotel.objects.get(id=identifier)
	images = Image.objects.get(hotel=hotel)
	try:
		language = request.POST.get('language')
	except:
		pass
	if language:
		hotel.body = getlanguage(language, hotel.name)
	for count in range(5):
		try:
			img_list += [(images.url_image.split(" ")[count], count+1)]
		except IndexError:
			pass
	comments = Comment.objects.all()
	for comment in comments:
		if comment.hotel == hotel:
			comment_list += [comment]
	template = get_template('hotel_id.html')
	context = RequestContext(request, {'hotel' : hotel,'hotel.body' : hotel.body,
										'img_list' : img_list, 'comments' : comment_list})
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
	favs = Favourite.objects.filter(user=user)
	for fav in favs:
		image = Image.objects.get(hotel=fav.hotel)
		img_list = image.url_image.split(" ")
		fav_list += [(fav, img_list)]
	template = get_template('xml/user_xml.xml')
	context = RequestContext(request, {'hotels' : fav_list})
	return HttpResponse(template.render(context), content_type="text/xml")

#Config section!
def saveconf(request):
	user = request.user.username
	color = request.POST.get('color')
	size = request.POST.get('size')
	if request.POST.get('title') is not None and request.POST.get('title') != "":
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

def about(request):
	template = get_template('about.html')
	user = request.user.username
	if request.user.is_authenticated():
		user = User.objects.get(username=user)
	context = RequestContext(request, {'user' : user})
	return HttpResponse(template.render(context))

#CSS serving here
def servecss(request):
	color = 'beige'
	size = 14
	template = get_template('css/index.css')
	if request.user.is_authenticated():
		user = request.user.username
		user = User.objects.get(username=user)
		config = Config.objects.get(user=user)
		color = config.color
		size = config.size
	context = RequestContext(request, {'color' : color, 'size' : size})
	return HttpResponse(template.render(context), content_type="text/css")

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

# authenticate user!
def auth(request):
	username = strip_tags(request.POST.get('username'))
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
	return HttpResponseRedirect('/')

def register(request):
	if request.method == "GET":
		template = get_template('registration/register.html')
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))
	elif request.method == "POST":
		username = request.POST.get('username')
		password = make_password(request.POST.get('password'))
		title = "Pagina de " + username
		user = User(username=username, password=password)
		user.save()
		user = User.objects.get(username=username)
		config = Config(user=user, title=title, color='beige', size=10)
		config.save()
		return HttpResponseRedirect("/")

def mainrss(request):
	hotel_list = []
	user_list = []
	ip = request.get_host()
	(hotel_list, user_list) = orderbycomments()
	template = get_template('rss/indexrss.rss')
	context = RequestContext(request, {'hotels' : hotel_list, 'ip' : ip,
										'users' : user_list})
	return HttpResponse(template.render(context))
