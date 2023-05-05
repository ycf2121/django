from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

# 继承AbstractUser表，应用auth模块
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    # 手机号
    telephone = models.CharField(max_length=32)
    # 用户头像
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.png')
    # 用户创建时间
    create_date = models.DateTimeField(auto_now_add=True)
    # 用户博客--一对一对应博客表
    blog = models.OneToOneField(to="Blog", to_field='nid', on_delete=models.CASCADE, null=True)


class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    # 博客名称
    title = models.CharField(max_length=32,verbose_name='博客名称')
    # 站点名称
    site_name = models.CharField(max_length=32,verbose_name='站点名称')
    # 博客主题样式
    theme = models.CharField(max_length=32,verbose_name='博客主题样式')

    def __str__(self):
        return self.title


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    # 分类名称
    title = models.CharField(max_length=32)
    # 所属博客
    blog = models.ForeignKey(to="Blog", to_field='nid', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    # 标签名称
    title = models.CharField(max_length=32)
    # 所属博客
    blog = models.ForeignKey(to="Blog", to_field='nid', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    # 文章标题
    title = models.CharField(max_length=32)
    # 文章摘要
    desc = models.CharField(max_length=255)
    # 存大文本
    # 文章内容
    content = models.TextField()
    # 创建时间
    create_date = models.DateTimeField(auto_now_add=True)

    comment_num = models.IntegerField(default=0)
    up_num = models.IntegerField(default=0)
    down_num = models.IntegerField(default=0)

    # user：跟user一对多
    # 文章作者
    user = models.ForeignKey(to='UserInfo', to_field='nid', null=True,on_delete=models.CASCADE)
    # category: 跟Category一对多
    # 文章分类
    category = models.ForeignKey(to='Category', to_field='nid', null=True,on_delete=models.CASCADE)
    # tag：跟Tag多对多
    # 文章标题（通过through指定自己写的中间表）
    tag = models.ManyToManyField(to='Tag', through='Article2Tag', through_fields=('article', 'tag'))


# 自己创建中间表，add(),remove(),set()不能用了
class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    # 文章id
    article = models.ForeignKey(to='Article', to_field='nid', null=True,on_delete=models.CASCADE)
    # 标签id
    tag = models.ForeignKey(to='Tag', to_field='nid', null=True,on_delete=models.CASCADE)


class ArticleUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    # 点赞/点踩 的用户
    user = models.ForeignKey(to='UserInfo', to_field='nid',on_delete=models.CASCADE)
    # 点赞/点踩 的文章
    article = models.ForeignKey(to='Article', to_field='nid', null=True,on_delete=models.CASCADE)
    # 赞还是踩
    is_up = models.BooleanField(default=True)


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    # 评论的用户
    user = models.ForeignKey(to='UserInfo', to_field='nid',on_delete=models.CASCADE)
    # 评论的文章
    article = models.ForeignKey(to='Article', to_field='nid',on_delete=models.CASCADE)
    # 评论的内容
    comm = models.CharField(max_length=255)
    # 评论的id
    create_date = models.DateTimeField(auto_now_add=True)

    # parent_comment=models.ForeignKey(to='Comment',to_field='nid')
    # 父评论的id，自关联，防止写脏数据
    parent_comment = models.ForeignKey(to='self', to_field='nid', null=True,on_delete=models.CASCADE)
