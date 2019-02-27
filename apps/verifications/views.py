import random

from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.yuntongxun.sms import CCP
from users.models import User
from verifications.serializers import UserSerializer


class SmsCodeView(APIView):
    def get(self, reqpuest, mobile):

        # 获取StrictRedis保存数据
        strict_redis = get_redis_connection('sms_codes')

         #1. 校验短信验证码是否重复发送(1分钟内禁止重复发送)
        send_flag = strict_redis.get('send_flag_%s'%mobile)
        if send_flag:
           raise ValidationError({'message': '频繁获取短信验证码'})
           # 2. 生成短信验证码
        # sms_code = '%06d' % random.randint(0, 999999)
        sms_code ='123456'

        strict_redis.setex('sms_codes_%s'%mobile,5*60,sms_code)
        strict_redis.setex('send_flag_%s'%mobile,60,1)

           # 3. 发送短信验证码(云通讯)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 5. 响应数据
        return Response({'message': 'OK' })


class ChecknameView(APIView):

    def get(self,request,username):
        count=User.objects.filter(username=username).count()


        data={
            'username':username,
            'count':count
        }

        return Response(data)


# class RegisterView(APIView):
#
#     def post(self,request):
#         # 1参数
#         dic_data=request.data
#         username=dic_data.get('username')
#         mobile=dic_data.get('mobile')
#         pw=dic_data.get('password')
#         pw2=dic_data.get('password2')
#         allow=dic_data.get('allow')
#         sms_code=dic_data.get('sms_code')
#
#         if not (username,pw,pw2,allow,sms_code):
#             return Response({'message':'参数不全'})
#
#         if pw !=pw2:
#             return Response({'message': '密码不一致'})
#
#         redis_store=get_redis_connection('sms_codes')
#
#         real_sms_code=redis_store.get('sms_codes_%s'%mobile).decode()
#
#         if real_sms_code !=sms_code:
#             return Response({'message': '验证码不对'})
#
#         user=User.objects.create_user(
#             username=username,
#             mobile=mobile,
#             password=pw
#         )
#
#         user_data=UserSerializer(user).data
#         return Response(user_data)

class RegisterView(CreateAPIView):

    serializer_class =UserSerializer



