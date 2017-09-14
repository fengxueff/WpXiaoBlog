#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'
from web.forms.base import BaseForm
from django import forms
from django.core.exceptions import ValidationError

class LoginForm(BaseForm,forms.Form):
    username = forms.CharField(min_length=6,
                               max_length=20,
                               error_messages={"required":"用户名不能为空",
                                               "min_length":"用户名长度不能小于6个字符",
                                               "max_length":"用户名长度不能超过20个字符"}
    )

    password = forms.RegexField(
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={"required":"密码不能为空",
                        "invalid":"密码必须包含数字、字母、特殊字符",
                        "min_length":"密码长度不能小于8个字符",
                        "max_length":"密码长度不能大于32个字符"
                        }
    )

    # False表示可以为空，True表示必须输入
    rmb = forms.IntegerField(required=False)

    check_code = forms.CharField(
        error_messages={"required":"验证码不能为空"}
    )


    # 当调用is_valid方法时会自动调用这个方法
    def clean_check_code(self):
        check_code = self.cleaned_data["check_code"]
        if self.request.session.get("CheckCode").upper() != self.request.POST.get("check_code").upper():
            raise ValidationError(message="验证码错误",code="invalid")
        else:
            return check_code
