from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^text/$',views.TestView2.as_view()),
]