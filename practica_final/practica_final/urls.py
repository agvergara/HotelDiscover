"""practica_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'hoteles.views.index'),
    url(r'^main/xml$', 'hoteles.views.mainxml'),
    url(r'^alojamientos$', 'hoteles.views.hotellist'),
    url(r'^alojamientos/(\d+)$', 'hoteles.views.hotel'),
    url(r'^admin/', admin.site.urls),
    #url(r'^(.*)&page=(\d+)$', 'hoteles.views.usernextpage'),
    url(r'^(.*)/xml$', 'hoteles.views.userxml'),
    url(r'^login/$', 'hoteles.views.register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^saveconf/$', 'hoteles.views.saveconf'),
    url(r'^addcomment/$', 'hoteles.views.addcomment'),
    url(r'^addfav/$', 'hoteles.views.addfav'),
    url(r'^(.*)$', 'hoteles.views.userpage'),
]
