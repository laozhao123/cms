from django.conf.urls import url

from goods import views

urlpatterns = [
    url(r'^top/$',views.TopGoods.as_view()),
    url(r'^cate/$',views.CateGoods.as_view()),
    url(r'^list/$',views.ListGoods.as_view()),
    url(r'^catelist/$',views.ListCatView.as_view()),
]