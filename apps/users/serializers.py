import re

from rest_framework import serializers

from news.models import News, NewsCategory
from users.models import Area, Address


class ProSerializer(serializers.ModelSerializer):
    class Meta:
        model=Area
        fields=('id','name')



class CitySerializer(serializers.ModelSerializer):

    subs=ProSerializer(many=True,read_only=True)
    class Meta:
        model = Area
        fields =('id','name','subs')


class AdresssSerializer(serializers.ModelSerializer):
    #默认返回外键id
    province=serializers.StringRelatedField(read_only=True)
    city=serializers.StringRelatedField(read_only=True)
    district=serializers.StringRelatedField(read_only=True)
    # 请求数据为id
    province_id=serializers.IntegerField(required=True)
    city_id=serializers.IntegerField(required=True)
    district_id=serializers.IntegerField(required=True)

    def validate_mobile(self, vaule):
        if not re.match('^1[39]\d{9}$',vaule):
            raise serializers.ValidationError('手机号格式错误')
        return vaule

    def create(self, validated_data):
        # 补充一个字段： 收件地址所属用户, 再保存到数据库表中
        user=self.context['request'].user
        validated_data['user']=user
        return super().create(validated_data)

    class Meta:
        model=Address
        # 新增地址，不需要用户传递user到服务器，服务器可以自动获取到当前登录用户对象
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')



class DelSerializer(serializers.ModelSerializer):

    pk =serializers.IntegerField(required=True,label='删除地址id')


    def validate_pk(self, value):
        user=self.context['request'].user
        try:
            Address.objects.get(id=value,user_id=user.id)
        except:
            raise serializers.ValidationError('地址不存在')

        return value


