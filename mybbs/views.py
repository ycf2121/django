from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import random
# pip3 install pillow
from PIL import Image,ImageDraw,ImageFont
# 内存管理，把图片放在内存里
from io import BytesIO

from django.contrib import auth

from mybbs import myforms

from mybbs.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
# Create your views here.

def login(request):
    #判断前台是否是ajax发过来的数据
    if request.is_ajax():
        back_msg={'user':None,'msg':None}
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        valid_code=request.POST.get('valid_code')
        print(name,pwd,valid_code)
        if valid_code.upper()==request.session.get('valid_code').upper():

            user= auth.authenticate(request,username=name,password=pwd)
            if user:
                auth.login(request,user)
                back_msg['user']=name
                back_msg['msg']='登陆成功'
            else:
                back_msg['msg']='用户名或密码错误'
        else:
            back_msg['msg'] = '验证码错误'
        return JsonResponse(back_msg)

    return render(request,'login.html')


def get_random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))


def get_code(request):
    # 方式一
    # with open('lhf.jpg','rb') as f:
    #     data=f.read()
    # 方式2
    # img=Image.new('RGB',(300,35),color='pink')
    #
    # with open('code.png','wb') as f:
    #     img.save(f,'png')
    # with open('code.png','rb') as f:
    #     data=f.read()

    img = Image.new('RGB', (300, 35), color=get_random_color())
    # 指定字体文件
    # font=ImageFont.truetype('static/font/kumo.ttf',30)
    font=ImageFont.truetype(r'static\font\QingNiaoHuaGuangJianMeiHei-2.ttf',30)
    draw=ImageDraw.Draw(img)
    valid_code=''
    for i in range(5):
        random_num=str(random.randint(0,9))
        random_upper=chr(random.randint(65,90))
        random_lower=chr(random.randint(97,122))
        random_chr=random.choice([random_num,random_upper,random_lower])
        draw.text((i*40+50, 3), random_chr, get_random_color(), font=font)
        valid_code+=random_chr

    # draw.text((5,5),'python',get_random_color(),font=font)
    print(valid_code)
    request.session['valid_code']=valid_code

    # 生成一个内存管理的对象
    f=BytesIO()
    # 把图片保存到内存中
    img.save(f, 'png')
    # 从内存中取出来
    data=f.getvalue()
    return HttpResponse(data)


def register(request):
    if request.is_ajax():
        back_msg={'user':None,'msg':None}
        name=request.POST.get('name')
        pwd=request.POST.get('pwd')
        re_pwd=request.POST.get('re_pwd')
        email=request.POST.get('email')
        myfile=request.FILES.get('myfile')
        print(request.POST)
        form_obj = myforms.RegForms(request.POST)
        if form_obj.is_valid():
            if myfile:
                UserInfo.objects.create_user(username=name,password=pwd,email=email,avatar=myfile)
            else:
                UserInfo.objects.create_user(username=name, password=pwd, email=email)
            back_msg['user']=name
            back_msg['msg']='注册成功'
        else:
            print(form_obj.errors)
            back_msg['msg'] = form_obj.errors
        return JsonResponse(back_msg)


    form_obj=myforms.RegForms()
    return render(request,'register.html',{'form_obj':form_obj})


def index(request):
    article_list=Article.objects.all()
    return render(request,'index.html',{'article_list':article_list})


def home_site(request,username,**kwargs):

    username=username
    # print(username)
    user=UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request,'error.html')
    # 第一种，基于对象的反向查询
    # article_list=user.article_set.all()
    # 第二种，基于双下划线的查询
    # article_list=Article.objects.filter(user__nid=user.nid)
    article_list = Article.objects.filter(user=user)
    print(kwargs)
    if kwargs:
        condition=kwargs.get('condition')
        if condition=='tag':
            search_tag=kwargs.get('param')
            article_list = Article.objects.filter(user=user).filter(tag__title=search_tag)
        elif condition=='category':
            search_tag = kwargs.get('param')
            article_list = Article.objects.filter(user=user).filter(category__title=search_tag)
        elif condition=='archive':
            # 2023-05
            search_tag = kwargs.get('param')
            year,month=search_tag.split('-')
            article_list = Article.objects.filter(user=user).filter(create_date__year=year,create_date__month=month)

    print(article_list)
    blog=user.blog
    # print(blog.title)
    # 查询当前站点下每个标签的文章数
    # 每个标签的文章数
    # tag_count=Tag.objects.all().annotate(c=Count('article__title')).values('title','c')
    # print(tag_count)
    # 查询当前站点下每个标签的文章数大于一的
    # tag_count=Tag.objects.filter(blog=blog).annotate(c=Count('article__title')).filter(c__gt=1).values('title','c')
    # 查询当前站点下每个标签的文章数
    # tag_count=Tag.objects.filter(blog=blog).annotate(c=Count('article__title')).values_list('title','c')
    # print(tag_count)
    # # 查询当前站点下每个分类的文章数
    # category_count=Category.objects.filter(blog=blog).annotate(c=Count('article__title')).values_list('title','c')
    # print(category_count)
    #
    # from django.db.models.functions import TruncMonth
    # mouth_list=Article.objects.all().filter(user=user).annotate(y_m=TruncMonth('create_date')).values('y_m').annotate(c=Count('y_m')).values_list('y_m','c')
    # print(mouth_list)
    # for i in ar_list:
    #     print(i.y_m)


    return render(request,'home_site.html',locals())


def article_detail(request,username,article_id):
    username=username
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    article=Article.objects.filter(pk=article_id).first()
    # 通过文章id拿出该文章所有的评论
    comment_list = Comment.objects.filter(article_id=article_id)

    return render(request,'article_deatil.html',locals())

import json
from django.db.models import F
def diggit(request):

    if request.is_ajax():
        back_msg={'status':None,'msg':None}
        if request.user.is_authenticated:
            article_id = request.POST.get('article_id')
            is_up = json.loads(request.POST.get('is_up'))
            print(type(is_up))
            ret=ArticleUpDown.objects.filter(article_id=article_id,user=request.user)
            if ret:
                back_msg['status']=False
                back_msg['msg']='您已经点过了'
            else:
                ArticleUpDown.objects.create(user=request.user,article_id=article_id,is_up=is_up)
                if is_up:
                    Article.objects.filter(pk=article_id).update(up_num=F("up_num")+1)
                    back_msg['msg'] = '点赞成功'
                else:
                    Article.objects.filter(pk=article_id).update(down_num=F("down_num") + 1)
                    back_msg['msg'] = '点踩成功'
                back_msg['status']=True
        else:
            back_msg['status'] = False
            back_msg['msg'] = '请先登录'

    return JsonResponse(back_msg)
    # return JsonResponse()


# 评论
def comment(request):
    back_msg = {'status':None}
    if request.is_ajax():

        if request.user.is_authenticated:
            user=request.user
            article_id=request.POST.get('article_id')
            content=request.POST.get('content')
            parent_id=request.POST.get('parent_id')
            if parent_id:
                # parent_id有值，取出父评论
                parent=Comment.objects.filter(pk=parent_id).first()

                back_msg['parent_user'] = parent.user.username
                back_msg['parent_comm'] = parent.comm
            ret=Comment.objects.create(user=user,article_id=article_id,comm=content,parent_comment_id=parent_id)
            back_msg['status']=True
            back_msg['user_name']=user.username
            # ret.create_date 日期对象 转成str
            # import datetime
            back_msg['create_time']=ret.create_date.strftime('%Y-%m-%d')
            back_msg['content']=content
        else:
            back_msg = {'status': False}




    return JsonResponse(back_msg)

@login_required(login_url='/login/')
def back_home(request):
    user=request.user
    article_list=Article.objects.filter(user=user)

    return render(request,'back/back_home.html',locals())

from bs4 import BeautifulSoup
@login_required(login_url='/login/')
def add_article(request):
    # Beautifulsoup4
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('article')
        #生成BeautifulSoup的对象，需要传两个参数，第一个参数是html的页面，第二个参数是解析页面用的方式
        # ss = '<p>aaa</p> <script>alert(123)</script>'
        soup=BeautifulSoup(content,'html.parser')

        ll=soup.find_all()
        for tag in ll:
            if tag.name =='script':
                tag.decompose()
        # print(str(soup))

        # soup.text取出html整个文本内容
        # print(soup.text)
        desc=soup.text[0:150]+'...'
        ret=Article.objects.create(user=request.user,title=title,content=str(soup),desc=desc)
        return redirect('/back_home/')

    return render(request,'back/add_article.html')


from BBS import settings
import os
def add_photo(request):
    print(request.FILES)
    if request.method =='POST':
        myfile=request.FILES.get('imgFile')
        path=os.path.join(settings.MEDIA_ROOT,'photo',myfile.name)

        with open(path,'wb') as f:
            for line in myfile:
                f.write(line)

    return JsonResponse({'error':0,'url':'/media/photo/'+myfile.name})