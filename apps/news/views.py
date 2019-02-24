from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from news.models import News
from news.serializers import NewSerializer


class Is_slideNews(APIView):
    def get(self,request):
        query_set=News.objects.filter(is_slide=1)

        s=NewSerializer(query_set,many=True)
        return Response(s.data)
