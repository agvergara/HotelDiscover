from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import strip_tags
from xmlparser import getHotels
from models import Hotel
import itertools
# Create your views here.

def loadhotels (url):
	parser = getHotels(url)
	#TODO: Arreglar que hay un elemento al final siempre que es vacio en el parser
	hotelname = parser.get('name').split(';;')[:-1]
	hoteladdress = parser.get('address').split(';;')[:-1]
	hotelweb = parser.get('web').split(';;')[:-1]
#	Parse/Map to float
	latitude = map(float, parser.get('latitude').split(';;')[:-1])
	longitude = map(float, parser.get('longitude').split(';;')[:-1])
	description = parser.get('body').split(';;')[:-1]
#	prueba = parser.get('item').split(';;')[-1]
#	print parser.get('item').split(';;')
	#Uso de itertools para utilizar las listas en paralelo
	#TESTING ALL THE VARIABLES, QUITAR PARA INTRODUCIR EN LA BASEDE DATOS!!!!!!!
	#AVISO
	#AVISO
	#AVISO
	#QUITAR EL COMENTARIO QUE TE VEO VENIR
	for name, address, web, latit, longit, descr in itertools.izip(hotelname, hoteladdress, hotelweb, latitude, longitude, description):
		#Strip HTML tags
		descr = strip_tags(descr)
		print "Saving: " + name
		hotel = Hotel(name=name, web=web, body=descr, address=address, latitude=latit, longitude=longit)
		hotel.save()



def index(request):

	urls = ''
	xml_language = {'spanish' : 'es', 'english' : 'en', 'french' : 'fr'}
	index = 'spanish'
	url = 'http://www.esmadrid.com/opendata/alojamientos_v1_' + xml_language[index] + '.xml'
	hotels = Hotel.objects.all()
	if not hotels:
		loadhotels(url)
	#Testing all the variables
#	loadhotels(url)
	return HttpResponse("Probando base de datos")