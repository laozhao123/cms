#默认只返回 token
import base64
import pickle
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django_redis import get_redis_connection

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):

    return {
        'token': token,
        'username':user.username,
        'id':user.id
    }


class UsernameMobileAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        判断用户名(手机号)或者密码是否正确，返回对应的用户对象。
        """
        query_set=User.objects.filter(Q(username=username) | Q(mobile=username))

        try:
            if query_set.exists():
                user=query_set.get() # 取出唯一的一条数据（取不到或者有多条数据都会出错）
                if user.check_password(password):  # 进入一步判断密码是否正确
                    return user
        except:
            return None

def merge_cart_cookie_to_redis(request, response, user):
    """
        合并cookie中的购物车数据到redis中
        :param request: 请求对象, 用于获取cookie
        :param response: 响应对象,用于清除cookie
        :param user: 登录用户, 用于获取用户id
        :return:
        """
    cart_cookie=request.COOKIES.get('cart')

    if not cart_cookie:
        return response
    # {2: {'count':1, 'selected':False}, 3: {'count':1, 'selected':False}}
    cart_data=  pickle.loads(base64.b64decode(cart_cookie.encode()))

    rs=get_redis_connection('cart')

    for sku_id,sku_id_dic in cart_data.items():
        count=sku_id_dic['count']
        selected=sku_id_dic['selected']

        rs.hset('cart_%s' % user.id, sku_id, count)

        if selected:
            rs.sadd('cart_selected_%s' % user.id, sku_id)
        else:
            rs.srem('cart_selected_%s' % user.id, sku_id)

    response.delete_cookie('cart')
    return response