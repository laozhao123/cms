from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from users import views

urlpatterns = [
    url(r'^text/$',views.TestView2.as_view()),
    # url('login/$', obtain_jwt_token),
    url('login/$', views.UserAuthorizeView.as_view()),
    url('areas/$', views.ProvinceView.as_view()),
    url('areas/(?P<pk>\d+)/$', views.CityView.as_view()),
    url('address/$', views.AddressView.as_view()),
    url('address/(?P<pk>\d+)/$', views.DeladdrressView.as_view()),
    url('setaddr/(?P<pk>\d+)/$', views.SetAddressView.as_view()),


]

# router=DefaultRouter()
#
# router.register('addresses',views.AddressView,base_name='addresses')
#
# urlpatterns += router.urls
