from . import views
from django.urls import path,re_path


urlpatterns = [
    path('content/<str:topic_name>/',
         views.ContentTopic, name='contentTopic'),
    path('', views.tutorial, name='tutorial'),
    path('post/update/<str:pk>/<slug:title>/',
         views.updatePost, name='updatePost'),
    path('post/<str:pk>/<slug:title>/',views.post,name='post'),
    path('post/delete/<str:pk>/<slug:title>/', views.deletePost,name='deletePost'),
    path('post/message/delete/<str:pk>/',views.deletePostMessage,name='deletePostMessage'),
  
    path('all-tutorial/',views.all_tutorial, name='all_tutorial'),
    path('activity/',views.activityPage,name="post_activity"),
    
    path('post/create/',views.createPost,name='createPost')
]
