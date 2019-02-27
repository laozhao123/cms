from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    url(r'^text/$',views.TestView2.as_view()),
    url('login/$', obtain_jwt_token),
]