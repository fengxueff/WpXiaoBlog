from django.db import models

# Create your models here.

class UserInfo(models.Model):
    """
        用户表
    """
    # 没有用AutoField字段说明该字段的长度后续有大量增加
    nid = models.BigAutoField(primary_key=True)

    username = models.CharField(max_length=32,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=64,verbose_name="密码")
    nickname = models.CharField(max_length=32,verbose_name="昵称")
    email = models.EmailField(unique=True,verbose_name="邮箱")
    avatar = models.ImageField(verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    fans = models.ManyToManyField(
                                    to="UserINfo",
                                    # 自定义第三张表
                                    through="UserFans",
                                    #反向操作时，使用的字段名，用于代替 【表名_set】 如： obj.表名_set.all()
                                    related_name="f",
                                    #与第三表之间的关联字段
                                    through_fields=("user","follower"),
                                    verbose_name="粉丝")


class UserFans(models.Model):
    """
        互粉多对多关系表
    """
    # 表示一个粉丝关注哪几个博主
    user = models.ForeignKey(to="UserInfo",to_field="nid",related_name="users",verbose_name="博主")
    # 表示一个博主拥有的粉丝数量
    follower = models.ForeignKey(to="UserInfo",to_field="nid",related_name="followers",verbose_name="粉丝")
    class Meta:
        # 定义联合唯一键
        unique_together = [("user","follower"),]

class Blog(models.Model):
    """
        博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64,verbose_name="个人博客标题")
    site = models.CharField(max_length=32,unique=True,verbose_name="个人博客前缀")
    theme = models.CharField(max_length=32,verbose_name="博客主题")
    user = models.OneToOneField(to="UserInfo",to_field="nid")

class Category(models.Model):
    """
        博主个人文章分类
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=32,verbose_name="分类标题")
    blog = models.ForeignKey(to="Blog",to_field="nid",verbose_name="所属博客")

class Tag(models.Model):
    """
        博客标签
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=128,verbose_name="文章标题")
    summary = models.CharField(max_length=255,verbose_name="文章简介")
    read_count = models.IntegerField(default=0,verbose_name="文章阅读量")
    comment_count = models.IntegerField(default=0,verbose_name="文章讨论量")
    up_count = models.IntegerField(default=0,verbose_name="点赞")
    down_count = models.IntegerField(default=0,verbose_name="嘘声")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    blog = models.ForeignKey(to="Blog",to_field="nid",verbose_name="所属博客")
    category = models.ForeignKey(to="Category",to_field="nid",verbose_name="文章分类")

    type_choice = [
        (1,"Python"),
        (2,"Linux"),
        (3,"OpenStack"),
        (4,"GoLang"),
    ]

    article_type_id = models.IntegerField(choices=type_choice,default=None)
    #自定义多对多关系
    tags = models.ManyToManyField(to="Tag",through="Article2Tag",through_fields=("article","tag"))

class Article2Tag(models.Model):
    """
        文章与标签关系表
    """
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容')

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')
