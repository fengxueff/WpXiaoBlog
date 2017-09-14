#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'

from django.conf.urls import url
from web.views import account,home
urlpatterns = [
    url(r"^login/$",account.login),
    url(r"^check_code/$",account.check_code),
    url(r"^$",home.index),
    url(r'^all/(?P<article_type_id>\d+)/', home.index, name='index'),
    url(r"^article_add/$",home.article_add),
    url(r"^article_show/(?P<blog_site>\w+)/(?P<article_nid>\d+)/",home.article_show),
    url(r"^upload_img/",home.upload_img),
]