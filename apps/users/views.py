from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# def test(request):
#     response=HttpResponse('text')
#
#     response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
#     return response
from rest_framework import mixins
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, ListCreateAPIView, \
    GenericAPIView, DestroyAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from users.models import Area
from users.serializers import ProSerializer, CitySerializer, AdresssSerializer, DelSerializer
from users.utils import merge_cart_cookie_to_redis


class TestView2(APIView):
    def get(self,request):
        # a=10/0
        # response = Response({'message': 'get请求'})
        # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8080'
        return HttpResponse('text')


class ProvinceView(ListAPIView):

    serializer_class =ProSerializer
    queryset = Area.objects.filter(parent=None)


class CityView(RetrieveAPIView):

    serializer_class =CitySerializer
    queryset = Area.objects.all()


class AddressView(ListAPIView,CreateAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = AdresssSerializer

    def get_queryset(self):
        # 获取当前登录用户的地址
        # return Address.objects.filter(user=self.request.user, is_deleted=False)
        return self.request.user.addresses.filter(is_deleted=False)

    # 限制返回的地址个数
    def create(self, request, *args, **kwargs):
        count = request.user.addresses.count()
        if count >= 2:  # 每个用户最多不能超过2个地址
            return Response({'message': '地址个数已达到上限'}, status=400)
        return super().create(request, *args, **kwargs)

    # 自定义地址列表接口的返回响应参数
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'limit': 10,  # 最大地址个数
            'user_id': request.user.id,  # 用户id
            'default_address_id': request.user.default_address_id,  # 用户默认地址id
            'addresses': serializer.data  # 原有的地址列表数据
        })


class SetAddressView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,pk):

        user=request.user

        user.default_address_id=pk

        user.save()

        return Response({'message':'OK'})


class DeladdrressView(DestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = DelSerializer

    def get_queryset(self):
        return self.request.user.addresses


#修改登陆后 合并cookie
class UserAuthorizeView(ObtainJSONWebToken):


    def post(self, request, *args, **kwargs):

        response=super().post(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user')

            response=merge_cart_cookie_to_redis(request, response, user)

        return response