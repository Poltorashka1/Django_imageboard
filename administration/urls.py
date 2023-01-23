from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('all_func/', views.all_func_view, name='all_func'),
    path('check_post/', views.all_unverified_post, name='check_post'),
    path('check_all_post/', views.all_post, name='all_post'),
    path('check_all_post/<board>/', views.all_post, name='board'),
    path('admin_decision/<int:pk>/<slug:slug>/<str:action>/', views.decision, name='decision'),
    path('comment/delete/<int:pk>/<str:action>/<slug:slug>/<int:post_pk>/', views.delete_comment,
         name='delete_comment'),
    path('change_user/', views.check_user, name='check_user'),
    path('deactive_user/<str:username>/<int:pk>/<str:action>/', views.deactive_user, name='deactive_user')
]
