

from django import template
from mybbs.models import *
from django.db.models import Count
from django.db.models.functions import TruncMonth
register=template.Library()

@register.inclusion_tag('classify.html')
def classify(username):
    # username=username
    # print(username)
    user = UserInfo.objects.filter(username=username).first()
    # if not user:
    #
    blog=user.blog
    # print(blog.title)
    tag_count=Tag.objects.filter(blog=blog).annotate(c=Count('article__title')).values_list('title','c')
    # print(tag_count)
    # 查询当前站点下每个分类的文章数
    category_count=Category.objects.filter(blog=blog).annotate(c=Count('article__title')).values_list('title','c')
    # print(category_count)

    month_list=Article.objects.all().filter(user=user).annotate(y_m=TruncMonth('create_date')).values('y_m').annotate(c=Count('y_m')).values_list('y_m','c')
    # print(month_list)

    return {'tag_count':tag_count,'category_count':category_count,'month_list':month_list,'blog':blog,'username':username}