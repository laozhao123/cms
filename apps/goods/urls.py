from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^top/$',views.TopGoods.as_view()),
    url(r'^cate/$',views.CateGoods.as_view()),
]