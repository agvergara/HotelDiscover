#!/usr/bin/python
# -*- coding: utf-8 -*-

#XML Parser given an url

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from xml.sax.saxutils import escape, unescape
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.data = {'name': '', 'web': '', 'address': '', 'latitude': '', 'longitude': '',
                     'body': '', 'images': [], 'category': []}
        self.imagelist = []
        self.categorylist = []
        self.section = ['basicData', 'geoData', 'multimedia', 'categoria']
        self.inSection = [0] * len(self.section)
        self.tags = ['name', 'web', 'body', 'address', 'latitude', 'longitude', 'url', 'item']
        self.inTags = [0] * len(self.tags)
        self.theContent = ""
        #Some flags for really special tags <3
        self.imageflag = False
        self.itemflag = False
        #Dis one for empty tags >3<
        self.flag = False

    def startElement(self, name, attrs):
        if name in self.section:
            self.inSection[self.section.index(name)] = 1
            self.flag = True
        elif self.inSection:
            if name in self.tags:
                self.inTags[self.tags.index(name)] = 1
                self.flag = False

    def endElement(self, name):
        position = 0
        if name in self.section:
            if self.inSection[2] and self.flag:
                self.data['images'] += [[""]]
            self.inSection[self.section.index(name)] = 0
        elif self.inTags:
            #Position of the tag
            for i,j in enumerate(self.inTags):
                if j == 1:
                    position = i
                    break
            if name == self.tags[position]:
                if name == 'url':
                    self.imagelist.append(self.theContent)
                    self.imageflag = True
                elif name == 'item':
                    self.categorylist.append(self.theContent)
                    self.itemflag = True
                else:
                    try:
                        self.data[name] += self.theContent + ';;'
                    except KeyError:
                        pass
                    if self.imageflag:
                        self.data['images'] += [self.imagelist]
                        self.imagelist = []
                        self.imageflag = False
                    elif self.itemflag:
                        self.categorylist = [self.categorylist[3], self.categorylist[5]]
                        self.data['category'] += [self.categorylist]
                        self.categorylist = []
                        self.itemflag = False
            self.theContent = ""
            try:
                self.inTags[self.tags.index(name)] = 0
            except ValueError:
                pass
        self.flag = False

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
            "&Ocirc;" : u'Ô',
            "&ocirc;" : u"ô",
            "&uuml;" : u'ü',
            "&Uuml;" : u'Ü',
            "&nbsp;" : '\n',
            "&rdquo;" : '"',
            "&ldquo;" : '"',
            "&lsquo;" : "'",
            "&rsquo;" : "'",
        }
        if self.inTags:
            text = self.theContent + chars
            self.theContent = unescape(text, html_escape_table)

def getHotels(url):
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    theParser.parse(url)
    # Fill the last imagelist and categorylist, for reasons
    theHandler.data['images'] += [theHandler.imagelist]
    theHandler.data['category'] += [[theHandler.categorylist[3], theHandler.categorylist[5]]]
    # RETURN ALL THE DATA  ヽ( ᗒ ѽ ᗕ )ﾉ
    return (theHandler.data)

#print getHotels('http://www.esmadrid.com/opendata/alojamientos_v1_es.xml')
