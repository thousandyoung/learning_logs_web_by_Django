from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from . import views
app_name = "users"
urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logut/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register, name='register'),
]
