#!/usr/bin/python
#-*- coding: utf-8 -*-


'''

'''
__author__ = 'wpxiao'

from django.shortcuts import render,HttpResponse,redirect
from web import models
from django.urls import reverse
from utils import pagination_new
def index(request,*args,**kwargs):
    article_type_list = models.Article.type_choice
    if kwargs:
        article_type_id = int(kwargs["article_type_id"])
        base_url = reverse("index",kwargs=kwargs)
        print(base_url)
    else:
        article_type_id = None
        base_url = "/"
    # 获取文章分类的数量
    data_count = article_list = models.Article.objects.filter(**kwargs).count()

    page_obj = pagination_new.Pagination(current_page=request.GET.get("p"),data_count=data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)
    print(request.session["user_info"])
    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )

from web.forms import article
from django.db import transaction
from utils.xss import XSSFilter
def article_add(request):
    if request.method == "GET":
        articleForm = article.ArticleForm(request)
        return render(request,"article_add.html",{"articleForm":articleForm})
    elif request.method == "POST":
        articleForm = article.ArticleForm(request=request,data=request.POST)
        if articleForm.is_valid():
            # 开启事务操作
            with transaction.atomic():
                tags = articleForm.cleaned_data.pop("tags")
                content = articleForm.cleaned_data.pop("content")
                content = XSSFilter().process(content)
                articleForm.cleaned_data["blog_id"] = request.session["user_info"]["blog__nid"]
                #创建文章
                article_obj = models.Article.objects.create(**articleForm.cleaned_data)
                # models.ArticleDetail.objects.create(content=content,article=article_obj)
                #功能同上，创建文章详细内容
                models.ArticleDetail.objects.create(content=content, article_id=article_obj.nid)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id = article_obj.nid,tag_id=tag_id))
                # 批量创建文章与标签关系，如果不调用批量创建接口的话，那就需要手动save
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect("/")
        else:
            # 表单验证错误的情况
            return render(request, "article_add.html", {"articleForm": articleForm})

def article_show(request,**kwargs):
    blog_site = kwargs.pop("blog_site")
    article_nid = int(kwargs.pop("article_nid"))
    article_obj = models.Article.objects.filter(nid=article_nid,blog__site=blog_site).first()
    # 一对一关系的反向查询
    article_content = article_obj.articledetail.content
    print(article_content)
    return render(request,"article_show.html",{"article_obj":article_obj,"article_content":article_content})

def upload_img(request):
    print("..........")
    result = {"error":0,"url":None}
    if request.method == "POST":
        dir = request.GET.get("dir",None)
        if dir == "image":
            img_obj = request.FILES.get("imgFile", None)
            print("img_obj:", img_obj.name)
            import os, json
            img_path = os.path.join("static/imgs/upload_img", img_obj.name)
            with open(img_path, mode="wb") as f:
                for i in img_obj.chunks():
                    f.write(i)
                result["url"] = "/static/imgs/upload_img/" + img_obj.name
            return HttpResponse(json.dumps(result))