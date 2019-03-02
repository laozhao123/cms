from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsAlbum


class CartSerializer(serializers.Serializer):
    """
    购物车数据序列化器
    """
    sku_id = serializers.IntegerField(label='sku id ', min_value=1)
    count = serializers.IntegerField(label='数量', min_value=1)
    selected = serializers.BooleanField(label='是否勾选', default=True)

    def validate(self, data):
        try:
            sku = Goods.objects.get(id=data['sku_id'])
        except Goods.DoesNotExist:
            raise serializers.ValidationError('商品不存在')
        return data


class CartSKUSerializer(serializers.ModelSerializer):

    count=serializers.IntegerField(label='数量')
    selected=serializers.BooleanField(label='是否勾选')

    class Meta:
        model=Goods
        fields=('id', 'title', 'img_url', 'sell_price', 'count', 'selected')