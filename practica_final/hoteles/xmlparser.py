#!/usr/bin/python
# -*- coding: utf-8 -*-

#XML Parser given an url

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.saxutils import escape, unescape
import sys

class myContentHandler(ContentHandler):

    #Si quiere añadir etiquetas, secciones o cosas a devolver, solo tengo que indicarlo aqui! :)
    def __init__ (self):
        self.data = {'name': '', 'web': '', 'address': '', 'latitude': '', 'longitude': '', 'body': ''}
        self.section = ['basicData', 'geoData']
        self.inSection = [0] * len(self.section)
        self.etiquetas = ['name', 'web', 'body', 'address', 'latitude', 'longitude']
        self.inEtiquetas = [0] * len(self.etiquetas)
        self.theContent = ""

    def startElement(self, name, attrs):
        if name in self.section:
            self.inSection[self.section.index(name)] = 1
        elif self.inSection:
            if name in self.etiquetas:
                self.inEtiquetas[self.etiquetas.index(name)] = 1

    def endElement(self, name):
        position = 0
        if name in self.section:
            self.inSection[self.section.index(name)] = 0
        elif self.inEtiquetas:
            #Posicion de la etiqueta
            for i,j in enumerate(self.inEtiquetas):
                if j == 1:
                    position = i
                    break
            if name == self.etiquetas[position]:
                self.data[name] += self.theContent + ';;'
            self.theContent = ""
            try:
                self.inEtiquetas[self.etiquetas.index(name)] = 0
            except ValueError:
                pass

    def characters (self, chars):
        html_escape_table = {
            "&quot;" : '"',
            "&apos;" : "'",
            "&iexcl" : u'¡',
            "&iquest" : u'¿',
            "&aacute;" : u'á',
            "&iacute;" : u'í',
            "&oacute;" : u'ó',
            "&uacute;" : u'ú',
            "&eacute;" : u'é',
            "&ntilde;" : u'ñ',
            "&Ntilde;" : u'Ñ',
            "&Aacute;" : u'Á',
            "&Iacute;" : u'Í',
            "&Oacute;" : u'Ó',
            "&Uacute;" : u'Ú',
            "&Eacute;" : u'É',
            "&nbsp;" : '\n',
        }
        if self.inEtiquetas:
            text = self.theContent + chars
            self.theContent = unescape(text, html_escape_table)

#Returns the 'html' variable from 'myContentHandler'
def getHotels(url):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse(url)
    return (theHandler.data)

#print getHotels('http://www.esmadrid.com/opendata/alojamientos_v1_es.xml')