#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from web import models

class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={"class":"form-control","placeholder":"文章标题"})
    )
    summary = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={"class":"form-control","placeholder":"文章简介","rows":"3"})
    )
    content = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={"class":"kind-content","cols":40,"rows":20})
    )
    article_type_id = django_fields.IntegerField(
        widget=django_widgets.RadioSelect(choices=models.Article.type_choice)
    )
    category_id = django_fields.ChoiceField(
        choices=[],
        widget=django_widgets.RadioSelect
    )
    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple
    )

    def __init__(self,request,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        blog_id = request.session["user_info"]["blog__nid"]
        print(models.Category.objects.filter(blog_id=blog_id).values("nid","title").query)
        #从数据库中查证出来初始化下拉列表框
        self.fields["category_id"].choices = models.Category.objects.filter(blog_id=blog_id).values_list("nid","title")
        self.fields["tags"].choices = models.Tag.objects.filter(blog_id=blog_id).values_list("nid","title")