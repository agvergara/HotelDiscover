#!/usr/bin/python
# -*- coding: utf-8 -*-
from xmlparser import getHotels
from models import Hotel, Image
from django.utils.html import strip_tags
import itertools

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

def getlanguaje(hotel_list, name, description):
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
		return getlanguaje(hotelname, name, description)
