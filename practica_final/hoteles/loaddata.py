#!/usr/bin/python
# -*- coding: utf-8 -*-
from xmlparser import getHotels
from models import Hotel, Image, Comment, Config, Favourite
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.db.models import Count
import itertools
import math

def load(hotelname, hoteladdress, hotelweb, latitude, longitude, description, imagelist, categorylist):
	#itertools to work with multiple lists at once
	for name, address, web, latit, longit, descr, category, images in itertools.izip(hotelname, hoteladdress, hotelweb, latitude, longitude, description, categorylist, imagelist):
		#Strip HTML tags
		descr = strip_tags(descr)
		print "Saving: " + name
		hotel = Hotel(name=name, web=web, body=descr, address=address, category=category[0],
			          latitude=latit, longitude=longit, stars=category[1])
		hotel.save()
		identifier = Hotel.objects.get(name=name)
		urls =' '.join(images)
		images = Image(hotel=identifier, url_image=urls)
		images.save()

def getlanguage(hotel_list, name, description):
	position = 0
	for i, hotel in enumerate(hotel_list):
		if hotel == name:
			position = i
			break
	body = strip_tags(description[position])
	return body


def loadhotels (url, flag, name):
	parser = getHotels(url)
	hotelname = parser.get('name').split(';;')[:-1]
	hoteladdress = parser.get('address').split(';;')[:-1]
	hotelweb = parser.get('web').split(';;')[:-1]
#	Parse/Map to float
	latitude = map(float, parser.get('latitude').split(';;')[:-1])
	longitude = map(float, parser.get('longitude').split(';;')[:-1])
	description = parser.get('body').split(';;')[:-1]
	imagelist = parser.get('images')
	categorylist = parser.get('category')
	if not flag:
		load(hotelname, hoteladdress, hotelweb, latitude, longitude, description, imagelist, categorylist)
	else:
		return getlanguage(hotelname, name, description)

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

def orderbycategory(request, categoryflag, category, starsflag, stars):
	hotel_list = []
	hotels = Hotel.objects.all()
	if categoryflag and starsflag:
		pass
	elif categoryflag: #Busca por stars
		hotels = Hotel.objects.filter(stars=stars)
	elif starsflag: #Busca por category
		hotels = Hotel.objects.filter(category=category)
	else:
		hotels = Hotel.objects.filter(category=category).filter(stars=stars)
	for hotel in hotels:
		hotel_list += [(hotel.name, hotel.id)]
	return hotel_list

def favourites (user, minpage, maxpage):
	hotel_list = []
	user = User.objects.get(username=user)
	favourites = Favourite.objects.filter(user=user)
	for fav in favourites:
		if minpage < maxpage:
			try:
				image = Image.objects.get(hotel=favourites[minpage].hotel)
				url = image.url_image.split(" ")[0]
				hotel_list += [(favourites[minpage].hotel, url, favourites[minpage].date)]
				minpage += 1
			except IndexError:
				break
	return (hotel_list, user)

def manypages(user):
	num_list = []
	num_favs = Favourite.objects.filter(user=user).count()
	max_pg = int(math.ceil((num_favs/10.0)))
	for num in range(max_pg):
		num_list += [num + 1]
	return (num_list, num_favs)
