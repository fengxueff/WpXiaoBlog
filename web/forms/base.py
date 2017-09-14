#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'

# 扩展Form的属性列表，可以将views中的request请求传入到Forms中
class BaseForm(object):
    def __init__(self,request,*args,**kwargs):
        self.request = request
        super(BaseForm,self).__init__(*args,**kwargs)