#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup


class XSSFilter(object):
    __instance = None

    def __init__(self):
        # XSS白名单
        self.valid_tags = {
            "font": ['color', 'size', 'face', 'style'],
            'b': [],
            'div': [],
            "span": [],
            "table": [
                'border', 'cellspacing', 'cellpadding'
            ],
            'th': [
                'colspan', 'rowspan'
            ],
            'td': [
                'colspan', 'rowspan'
            ],
            "a": ['href', 'target', 'name'],
            "img": ['src', 'alt', 'title'],
            'p': [
                'align'
            ],
            "pre": ['class'],
            "hr": ['class'],
            'strong': []
        }

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param cls:
        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instance:
            obj = object.__new__(cls, *args, **kwargs)
            cls.__instance = obj
        return cls.__instance

    def process(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        # 遍历所有HTML标签
        for tag in soup.find_all(recursive=True):
            # 判断标签名是否在白名单中
            if tag.name not in self.valid_tags:
                tag.hidden = True
                if tag.name not in ['html', 'body']:
                    tag.hidden = True
                    tag.clear()
                continue
            # 当前标签的所有属性白名单
            xx = tag.name
            attr_rules = self.valid_tags[tag.name]
            keys = list(tag.attrs.keys())
            if tag.name == "img":
                keys = list(tag.attrs.keys())
                for key in keys:
                    if key == "src":
                        tag[key] = re_imgpath("/static/imgs/upload_img/",tag.attrs[key])

            for key in keys:
                if key not in attr_rules:
                    del tag[key]

        return soup.decode()

import re
import os
def re_imgpath(path,img):
    pre_img= img
    s = re.split("/", img)
    if s[len(s) - 1]:
        img = s[len(s) - 1]
    else:
        img = s[len(s) - 2]
    load_img("static/imgs/upload_img/",pre_img,img)
    return os.path.join(path,img)

import requests
def load_img(path,pre_img,save_img):
    print(path)
    print(pre_img)
    print(save_img)
    img_obj = requests.get(pre_img)
    with open(os.path.join(path,save_img),"wb") as f:
        for i in img_obj:
            f.write(i)


if __name__ == '__main__':
    html = """<p class="title">
                        <b>The Dormouse's story</b>
                    </p>
                    <p class="story">
                        <div name='root'>
                            Once upon a time there were three little sisters; and their names were
                            <a href="http://example.com/elsie" class="sister c1" style='color:red;background-color:green;' id="link1"><!-- Elsie --></a>
                            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                            <a href="http://example.com/tillie" class="sister" id="link3">Tilffffffffffffflie</a>;
                            and they lived at the bottom of a well.
                            <script>alert(123)</script>
                        </div>
                        <img class=" " src="https://note.wiz.cn/wiz-resource/a5407b66-cfd7-4d33-b3e7-90908ed1eeaf/ddb31d35-6d7b-4ba1-809f-50cf1253b57a/index_files/0.jpg" style="height:auto !important;" /> 
                    </p>
                    <p class="story">...</p>"""

    obj = XSSFilter()
    v = obj.process(html)
    print(v)