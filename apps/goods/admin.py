from django.contrib import admin

# Register your models here.
# 注册Model类
from goods.models import Goods

admin.site.register(Goods)