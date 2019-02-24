import random

from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from libs.yuntongxun.sms import CCP






class SmsCodeView(APIView):
    def get(self, reqpuest, mobile):

    # 获取StrictRedis保存数据
        strict_redis = get_redis_connection('sms_codes')

         #1. 校验短信验证码是否重复发送(1分钟内禁止重复发送)
        send_flag = strict_redis.get('send_flag_%s')
        if send_flag:
           raise ValidationError({'message': '频繁获取短信验证码'})
           # 2. 生成短信验证码
        # sms_code = '%06d' % random.randint(0, 999999)
           sms_code ='123456'


           # 3. 发送短信验证码(云通讯)
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        # 5. 响应数据
        return Response({'message': 'OK'})
