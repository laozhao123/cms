from django.conf.urls import url

from news import views

urlpatterns = [
    url(r'^top/$',views.TopNews.as_view()),
    url(r'^cate/$',views.CateNews.as_view()),
]