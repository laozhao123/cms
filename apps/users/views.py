from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# def test(request):
#     response=HttpResponse('text')
#
#     response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
#     return response
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView2(APIView):
    def get(self,request):
        # a=10/0
        # response = Response({'message': 'get请求'})
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return HttpResponse('text')