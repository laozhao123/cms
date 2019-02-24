from django_redis import get_redis_connection
from rest_framework.views import APIView


class SmsCodeView(APIView):
    def get(self, reqpuest, mobile):

    # 获取StrictRedis保存数据
    strict_redis = get_redis_connection('sms_codes')

    #4. 校验短信验证码是否重复发送(1分钟内禁止重复发送)

