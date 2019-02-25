from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News, NewsCategory
from news.serializers import NewsSerializer, CatSerializer


class TopNews(APIView):
    def get(self,request):
        slide_news=News.objects.filter(is_slide=1).exclude(img_url='')
        top_news=News.objects.order_by('-create_time')[:10]
        img_news=News.objects.order_by('-click').exclude(img_url='')[:4]

        slide_news=NewsSerializer(slide_news,many=True).data
        top_news=NewsSerializer(top_news,many=True).data
        img_news=NewsSerializer(img_news,many=True).data

        data={
            'slide_news':slide_news,
            'top_news':top_news,
            'img_news':img_news,
        }

        return Response(data)

# [{
#     id:1,
#     "title":xxxx,
#     cate_set:[
#         {id,title},{},{}
#     ]
#      news:[]
#         top8:[]
#
#
# }
#     ...
#
#
# ]
class CateNews(APIView):

    def get(self,reqeust):
        bcats=NewsCategory.objects.filter(parent=0)
        # bcats_data=CatSerializer(bcats,many=True).data
        b_cats_list=[]
        for bcat in bcats:

            scats=bcat.newscategory_set.all()
            bcat = CatSerializer(bcat).data
            ids=[]
            for scat in scats:
                ids.append(scat.id)
            news=News.objects.filter(category_id__in=ids).exclude(img_url='').order_by('-create_time')[:4]
            news=NewsSerializer(news,many=True).data
            bcat['news']=news
            top8 = News.objects.filter(category_id__in=ids).order_by('-create_time')[:8]
            top8 = NewsSerializer(top8, many=True).data
            bcat['top8'] = top8

            b_cats_list.append(bcat)




        return Response(b_cats_list)
