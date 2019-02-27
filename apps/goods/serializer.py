from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsAlbum


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Goods
        fields='__all__'


class SonSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsCategory
        fields=('id','title')

class CateSerializer(serializers.ModelSerializer):

    goodscategory_set=SonSerializer(many=True)

    class Meta:
        model=GoodsCategory
        fields=('id','title','goodscategory_set')


class GoodsAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model=GoodsAlbum
        fields=('__all__')

