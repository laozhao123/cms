from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import Goods, GoodsCategory
from goods.serializer import GoodsSerializer, CateSerializer


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