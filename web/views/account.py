from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

from io import BytesIO
from utils.check_code import create_validate_code
# 验证码请求处理
def check_code(request):
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, "PNG")
    request.session["CheckCode"] = code
    return HttpResponse(stream.getvalue())

from web.forms.account import LoginForm
import json
from web import models
#登录请求
def login(request):
    if request.method == "GET":
       if request.session.get("user_info",None):
            return redirect("/")
       else:
            return render(request,"login.html")

    elif request.method == "POST":
        # 定义返回数据以供客户端ajax调用
        result = {"status":False,"message":None,"data":None}
        # 将数据与请求发送到form中进行数据格式以及自定义验证
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user_info = models.UserInfo.objects.filter(username=username,password=password)\
                        .values('nid', 'nickname',
                                'username', 'email',
                                'avatar',
                                'blog__nid',
                                'blog__site').first()
            if not user_info:
                result["message"] = "用户名或密码错误"
            else:
                result["status"] = True
                request.session["user_info"] = user_info
                if form.cleaned_data.get("rmb"):
                    # 会话保留七天
                    request.session.set_expiry(60*60*24*7)
        else:
            print(form.errors)
            if "check_code" in form.errors:
                # result["message"] = "验证码错误或过期"
                result["message"] = form.errors["check_code"]
            else:
                result["message"] = "用户名或密码错误"
        return HttpResponse(json.dumps(result))


