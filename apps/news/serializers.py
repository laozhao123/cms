import os
from collections import OrderedDict

from django.template import loader

from cms import settings
from news.models import News, NewsCategory

"""
# 商品频道及分类菜单: ordered_dict.values  --> 列表
'''
ordered_dict = {
    1: {
        'channels': [{手机}, {相机}, {数码}],  # 一级类别
        'sub_cats': [
            {'id':, 'name':手机通讯, 'sub_cats': [{手机}, {手机游戏},...]}, # 二级类别
            {'id':, 'name':手机配件, 'sub_cats': [{手机壳},{}...]},    # 二级类别

            {'id':, 'name':摄影相机, 'sub_cats': [{.},{.}...]},    # 二级类别
"""

def get_categories():
    lst=[]
    bcats=NewsCategory.objects.filter(parent=0)
    for bcat in bcats:
        scats=bcat.newscategory_set.all()
        bcat.sub_cats=scats
        lst.append(bcat)
    return lst

def generate_static_news_html():

    lst=get_categories()
    # 轮播图新闻，推荐新闻，图片新闻，类别新闻
    lunbonews=News.objects.filter(is_slide=1)
    tuijiannews=News.objects.order_by('-create_time')[:10]
    urlsnews = News.objects.filter(img_url__isnull=True).order_by('-click')[:4]

    # 3. 使用django模型语法渲染模板,得到静态的首页内容
    context={
        'lunbonews':lunbonews,
        'tuijiannews':tuijiannews,
        'urlsnews':urlsnews,
        'lst':lst,
    }

    temp=loader.get_template('news.html')
    html_text = temp.render(context)

    # 4. 把首页内容写到 front_end_pc/index.html 文件中
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'news.html')
    with open(file_path,'w') as f:
        f.write(html_text)