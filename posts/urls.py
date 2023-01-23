from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('<slug:board>/', views.post_list, name='list'),
    path('post/<slug:slug>/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.new_post, name="post_create"),
    path('post_edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('like/<int:pk>/<str:action>/', views.post_like, name='like'),
    path('post_search/search/', views.search, name='search'),
    path('post/reply/<slug:slug>/<int:pk>/<int:comment_id>/', views.post_detail, name='reply'),
]
