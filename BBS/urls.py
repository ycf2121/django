"""BBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from mybbs import views
from django.views.static import serve
from BBS import settings
urlpatterns = [
    url(r"^$", views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^get_code/$', views.get_code),
    url(r'^register/$', views.register),
    url(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"index", views.index),
    url(r"diggit", views.diggit),
    url(r"^comment/$", views.comment),
    url(r"^back_home/$", views.back_home),
    url(r"^add_article/$", views.add_article),
    url(r"^add_photo/$", views.add_photo),

    url(r"(?P<username>\w+)/articles/(?P<article_id>\d+)", views.article_detail),
    url(r"(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)", views.home_site),
    # url(r"(?P<username>\w+)/category/.*", views.home_site),
    # url(r"(?P<username>\w+)/archive/.*", views.home_site),
    url(r"(?P<username>\w+)", views.home_site),
]