'''learning_logs url model'''
from django.conf.urls import url
from . import views
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

app_name="learning_logs"
urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    url(r'^new_topic$', views.new_topic, name="new_topic"),
    url(r'^delete_topic/(?P<topic_id>\d+)$', views.delete_topic, name="delete_topic"),
    url(r'^new_entry/(?P<topic_id>\d+)$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry'),
    url(r'^show_entry/(?P<entry_id>\d+)/$', views.show_entry, name="show_entry"),
    url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name="delete_entry"),
    url(r'^search_entry/$', views.search_entry, name="search_entry"),


]
