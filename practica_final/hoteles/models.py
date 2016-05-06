from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    web = models.TextField()
    address = models.CharField(max_length=100)
   # category = models.CharField(max_length=20)
   # stars = models.IntegerField()
    body = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    def __unicode__(self):
		return self.name

class Image(models.Model):
	
    hotel_id = models.ManyToManyField('Hotel')
    url_image = models.TextField()
    def __unicode__(self):
    	return self.hotel_id

class Comment(models.Model):

    hotel_id = models.ManyToManyField('Hotel')
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    comment = models.TextField()
    #user = models.ForeignKey('Users')
    def __unicode__(self):
    	return self.hotel_id

class Config(models.Model):
    #user = models.ForeignKey('Users')
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    size = models.IntegerField()
