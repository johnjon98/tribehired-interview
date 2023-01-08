from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('posts', views.PostsView.as_view(), name='posts'),
    path('comments', views.CommentsView.as_view(), name='comments'),

]