from django.conf.urls import url


from verifications import views

urlpatterns = [
        url('sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsCodeView.as_view()),
        url('usernames/(?P<username>\w{5,20})/count/$', views.ChecknameView.as_view()),
        url('register/$', views.RegisterView.as_view()),

        ]