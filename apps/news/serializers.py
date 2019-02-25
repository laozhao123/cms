from rest_framework import serializers

from news.models import News, NewsCategory


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=News
        fields='__all__'

class SonCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields =('id','title')


class CatSerializer(serializers.ModelSerializer):
    newscategory_set=SonCatSerializer(many=True)
    class Meta:
        model = NewsCategory
        fields =('id','title','newscategory_set')

