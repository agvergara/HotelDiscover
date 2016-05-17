from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    web = models.TextField()
    address = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    stars = models.CharField(max_length=30)
    body = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    def __unicode__(self):
		return self.name

class Image(models.Model):

    hotel = models.ForeignKey('Hotel', default="")
    url_image = models.TextField()
    def __unicode__(self):
    	return unicode(self.hotel)

class Comment(models.Model):

    user = models.ForeignKey(User, default="")
    hotel = models.ForeignKey('Hotel', default="")
    title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(auto_now=True)
    comment = models.TextField(blank=True, null=True)
    def __unicode__(self):
    	return unicode(self.hotel)

class Config(models.Model):
    user = models.ForeignKey(User, default="")
    title = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return unicode(self.user)

class Favourite(models.Model):
    user = models.ForeignKey(User, default="")
    hotel = models.ForeignKey('Hotel', default="")
    date = models.DateField(auto_now=True)
    def __unicode__(self):
        return unicode(self.user)
