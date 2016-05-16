from django.contrib import admin
from models import Hotel, Image, Comment, Config, Favourite
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Config)
admin.site.register(Favourite)