from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Goods, GoodsCategory
from goods.serializer import GoodsSerializer, CateSerializer, SonSerializer


class TopGoods(APIView):
    def get(self,request):

        top=Goods.objects.filter(is_red=1)[:4]
        top=GoodsSerializer(top,many=True).data

        data={
            'is_red':top
        }

        return Response(data)



class CateGoods(APIView):
    def get(self,request):

        bcats=GoodsCategory.objects.filter(parent=0)
        # bcats=CateSerializer(bcats,many=True).data
        lis=[]
        for bcat in bcats:
            bcat_data=CateSerializer(bcat).data
            scats=bcat.goodscategory_set.all()
            ids=[]
            for scat in scats:
                ids.append(scat.id)
            goods=Goods.objects.filter(category_id__in=ids)[:5]
            goods=GoodsSerializer(goods,many=True).data

            bcat_data['goods']=goods

            lis.append(bcat_data)

        return Response(lis)


class ListGoods(APIView):

    def get(self,request):

        cat_id=request.query_params.get('category_id')
        ordering=request.query_params.get('ordering')

        cat=GoodsCategory.objects.get(id=cat_id)

        if cat.parent_id == 0:
            pass
        if ordering:
            goods=Goods.objects.filter(category_id=cat_id).order_by('-'+ordering).all()
        else:
            goods = Goods.objects.filter(category_id=cat_id).all()
        goods_data=GoodsSerializer(goods,many=True).data

        return Response(goods_data)


class ListCatView(APIView):

    def get(self,request):

        cat_id = request.query_params.get('category_id')

        cat=GoodsCategory.objects.get(id=cat_id)

        cat_par=cat.parent

        cat_data=SonSerializer(cat).data

        cat_data['parent']=''

        if cat_par:
            cat_data_par=SonSerializer(cat_par).data

            cat_data['parent']=cat_data_par

        return Response(cat_data)