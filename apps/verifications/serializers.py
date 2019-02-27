import re

from django_redis import get_redis_connection
from rest_framework import serializers

from news.models import News, NewsCategory
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    #验证字段
    allow=serializers.BooleanField(label='是否同意',write_only=True)
    sms_code=serializers.CharField(label='验证码',write_only=True)
    password2=serializers.CharField(label='密码2',write_only=True)


    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('请同意用户协议')
        return value


    def validate_mobile(self, value):
        if not re.match(r'^1[39]\d{9}$',value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate(self, attrs):
        if attrs['password2'] !=attrs['password']:
            raise serializers.ValidationError('密码不一致')

        sms_code=attrs['sms_code']

        redis_store=get_redis_connection('sms_codes')

        mobile=attrs['mobile']

        real_sms_code=redis_store.get('sms_codes_%s'%mobile)

        if not real_sms_code:
            raise serializers.ValidationError('短信验证码无效')

        if sms_code!=real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):

        return  User.objects.create_user(
            username=validated_data.get('username'),
            mobile=validated_data.get('mobile'),
            password=validated_data.get('password'),
        )

    class Meta:
        model=User
        fields=('id', 'username', 'password', 'password2',
                  'sms_code', 'mobile', 'allow')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }



