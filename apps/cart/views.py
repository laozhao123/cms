import base64

import pickle
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.serializer import CartSerializer, CartSKUSerializer
from goods.models import Goods


class addView(APIView):

    # permission_classes = [IsAuthenticated]
    #如果配置了jwt，前段带有jwt,就会执行下面函数先,再进入视图函数
    def perform_authentication(self, request):
        try:
            super().perform_authentication(request)
        except Exception as e:
            print('perform_authentication: ', e)



    def post(self, request):
        """
        添加购物车
        """
        # 创建序列化器，校验请求参数是否合法
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取请求参数
        sku_id = serializer.validated_data.get('sku_id')
        count = serializer.validated_data.get('count')
        selected = serializer.validated_data.get('selected')

        user = request.user
        if user.is_authenticated():  # 判断是否已登录
            # 用户已登录，在redis中保存
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()
            # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            # 增加购物车商品数量
            pl.hincrby('cart_%s' % user.id, sku_id, count)
            # 保存商品勾选状态
            if selected:
                pl.sadd('cart_selected_%s' % user.id, sku_id)
            pl.execute()
            return Response(serializer.data,status=201)
        else:
            # 1. 从cookie中获取购物车信息
            cart = request.COOKIES.get('cart')

            # 2. base64字符串 -> 字典
            # {1: {'count':2, 'selected':False}, 2: {'count':2, 'selected':False}}
            if cart is not None:
                cart = pickle.loads(base64.b64decode(cart.encode()))
            else:
                cart = {}
        print('cookies: ', cart)

        # 3. 新增字典中对应的商品数量
        sku = cart.get(sku_id)
        if sku:  # 原有数量 + 新增数量
            count += int(sku.get('count'))
        cart[sku_id] = {
            'count': count,
            'selected': selected
        }

        # 4. 字典 --> base64字符串
        cookie_cart = base64.b64encode(pickle.dumps(cart)).decode()

        # 5. 通过cookie保存购物车数据（base64字符串）
        response = Response(serializer.data, status=201)
        # 参数3：cookie有效期
        response.set_cookie('cart', cookie_cart)
        return response


    def get(self,request):

        user=request.user
        redis_store=get_redis_connection('cart')

        ha_data=redis_store.hgetall('cart_%s'%user.id) # 字典,键值为bytes {1: 2, 2: 2}
        s_data=redis_store.smembers('cart_selected_%s'%user.id)     # 列表 [1,  2]

        # 拼装字典
        # {1: {'count':2, 'selected':False}, 2:{'count':2, 'selected':False}}
        cart = {}
        for sku_id,count in ha_data.items():
            cart[int(sku_id)]={
                'count':int(count),
                'selected':sku_id in s_data
            }

        # 查询购物车中所有的商品
        skus=Goods.objects.filter(id__in=cart.keys())

        for sku in skus:
            # 给sku对象新增两个字段: 商品数量和勾选状态
            sku.count=cart[sku.id]['count']
            sku.selected=cart[sku.id]['selected']

        s=CartSKUSerializer(skus,many=True)


        return Response(s.data)


    def put(self,request):

        user=request.user

        redis_store=get_redis_connection('cart')

        s = CartSerializer(data=request.data)
        s.is_valid(raise_exception=True)

        # 获取请求参数
        sku_id = s.validated_data.get('sku_id')
        count = s.validated_data.get('count')
        selected = s.validated_data.get('selected')

        redis_store.hset('cart_%s' % user.id,sku_id,count)

        if selected:
            redis_store.sadd('cart_selected_%s' % user.id, sku_id)
        else:
            redis_store.srem('cart_selected_%s' % user.id, sku_id)

        return Response(s.data)


    def delete(self,request):
        user=request.user
        sku_id=request.data.get('sku_id')

        try:
            Goods.objects.get(id=sku_id)
        except:
            return Response({'message':'商品不存在'},status=400)


        rs=get_redis_connection('cart')

        rs.srem('cart_selected_%s' % user.id,sku_id)


        rs.hdel('cart_%s' % user.id,sku_id)

        return Response({'message':"ok"},status=204)







