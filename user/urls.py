from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view
from . import form

app_name = 'accounts'

urlpatterns = [
    path('login/', views.usr_login, name='login'),
    # path('password_reset/', views.forgot_password, name='password_reset'),
    path('reset_password/',
         auth_view.PasswordResetView.as_view(
             success_url=reverse_lazy('accounts:password_reset_done'), form_class=form.PasswordResetForm),
         # reverse_lazy без нее не работает
         name='reset_password'),
    path('reset_password_sent/',
         auth_view.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
         auth_view.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',
                                                    success_url=reverse_lazy('accounts:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_view.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<slug:account_url>/', views.profile, name='user_profile'),
    path('profile/user/edit', views.profile_update, name='profile_update'),
    path('activate/<str:uid>/<str:token>', views.activate, name='activate'),

    path('profile/subscribe/<account_url>/<str:action>/', views.subscribe, name='subscribe'),
    path('profile/subscribe/<account_url>/<str:action>/<redirec>', views.subscribe, name='subscribe'),

    path('profile/all_subscribers/<slug:account_url>/', views.subscribers, name='subscribers'),
    path('profile/sub_post/<slug:account_url>/', views.sub_post, name='sub_post'),
    path('profile/liked_post/all/', views.all_liked_post, name='all_liked_post'),
    path('profile/action/list/', views.action, name='action_list'),
    path('profile/post_from_subuser/all/', views.post_from_subuser, name='post_from_subuser')
    # path('reset_password/<str:uid>/<str:token>', views.reset, name='reset_password'),
]
