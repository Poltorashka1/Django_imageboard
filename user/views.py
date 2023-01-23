from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from slugify import slugify
from django.contrib.postgres.search import SearchVector
from . import form
from . import models
from actions.models import Action
from posts.models import Post
from django.contrib.auth import authenticate, login
from posts.models import Post
from .token import account_activation_token
from posts.form import SearchForm

CustomUser = get_user_model()


# Create your views here.

@login_required
def profile(request, account_url=None):
    """Отображение профиля пользователей"""
    if account_url:
        profile = get_object_or_404(CustomUser, account_url=account_url)
        if profile.username != request.user.username:
            posts = Post.objects.filter(author=profile.id, publish=True)
            return render(request, template_name="registration/profile1.html",
                          context={'profile': profile, 'posts': posts})
        else:
            posts = Post.objects.filter(author=profile.id, publish=True)
            return render(request, template_name="registration/profile1.html",
                          context={'profile': profile, 'section': 'profile', 'user_account': 'true', "posts": posts})
    else:
        profile = get_object_or_404(CustomUser, username=request.user.username)
        posts = Post.objects.filter(author=profile.id, publish=True)
        return render(request, template_name="registration/profile1.html",
                      context={'profile': profile, 'section': 'profile', 'user_account': 'true', "posts": posts})


@login_required
def profile_update(request):
    """Views для редактирования пользователя"""
    if request.method == "POST":
        user_form = form.UserInfoChangeForm(instance=request.user,
                                            data=request.POST,
                                            files=request.FILES)  # каким-то образом влияет на форму и не делает повторной отправки данных
        if user_form.is_valid():
            user_form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        user_form = form.UserInfoChangeForm(instance=request.user)
    return render(request, template_name='registration/profile.html',
                  context={'user_form': user_form, 'section': 'profile'})


def subscribe(request, account_url, action, redirec=None):
    """Подписка на пользователя"""
    user_to_sub = models.CustomUser.objects.get(account_url=account_url)
    if action == 'follow':
        models.Contact.objects.get_or_create(sub_user=user_to_sub, user_to_sub=request.user)
    if action == 'unfollow':
        models.Contact.objects.filter(user_to_sub=request.user, sub_user=user_to_sub).delete()
    else:
        pass

    if redirec == 'user_sub':
        return redirect('accounts:sub_post', account_url=request.user.account_url)
    else:
        return redirect('accounts:user_profile', account_url=user_to_sub.account_url)


def register(request):
    """Views для регистрации пользователя"""
    if request.method == 'POST':
        user_form = form.UserRegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.is_active = False
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = "Активация аккаунта"
            message = render_to_string('registration/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data['email']
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, template_name='registration/register_done.html', context={'new_user': new_user})
    else:
        user_form = form.UserRegisterForm()
    return render(request, template_name='registration/register.html', context={'user_form': user_form})


def usr_login(request):
    """Views для входа пользователя"""
    # To-do authenticate возвращает None если пользователь не активен, надо пофиксить
    if request.method == "POST":
        login_form = form.UserLoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        login_form = form.UserLoginForm()
    return render(request, 'registration/login.html', {'login_form': login_form})


def activate(request, uid, token):
    """Views для активации аккаунта"""
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirm = True
        user.save()
        login(request, user, backend='user.authentication.EmailAuthBackend')
        return redirect('accounts:profile')
    else:
        messages.error(request, "Ошибка")


def search(param, place):
    search_form = SearchForm(param.GET)
    if search_form.is_valid():  # Сделать валидацию формы для ускорения
        result = []
        query = search_form.cleaned_data['query']
        if place == "subscribers":
            result = param.user.following.filter(username=query)
        if place == 'sub_post':
            result = param.user.Подписчики.filter(username=query)
        if place == 'all_liked_post':
            result = Post.objects.filter(like=param.user.id).annotate(
                search=SearchVector('text', 'author_id__username', 'name'), ).filter(search=query)
        if place == 'post_from_subuser':
            result = Post.objects.filter(author__in=param.user.Подписчики.values_list('id', flat=True),
                                         publish=True).annotate(
                search=SearchVector('text', 'author_id__username', 'name'), ).filter(search=query).order_by(
                'author_id__username')

        if len(result):
            return result, True
        else:
            return result, False
    return None


@login_required()
def subscribers(request, account_url):
    """Выводит всех подписчиков пользователя"""
    search_form = SearchForm()
    result = []
    query = None
    if 'query' in request.GET:
        result, query = search(request, 'subscribers')
    user = models.CustomUser.objects.get(
        account_url=account_url)  # используем get так как у queryset не можем искать подписчиков
    # all_following = user.user_to_sub.all()
    # al_folowing = user.sub_user.all()
    all_following = user.following.all()  # Подписчики

    return render(request, template_name='registration/subscribers.html',
                  context={"all_following": all_following, 'user': user, 'result': result,
                           'search_form': search_form, 'query': query})


@login_required()
def sub_post(request, account_url):
    """Выводит Подписки пользователя"""
    search_form = SearchForm()
    result = []
    query = None
    if 'query' in request.GET:
        result, query = search(request, 'sub_post')
    user = models.CustomUser.objects.get(account_url=account_url)
    user_sub = user.Подписчики.all()  # Подписки
    return render(request, 'registration/sub_post.html', {'user_sub': user_sub, 'user': user, 'result': result,
                                                          'search_form': search_form, 'query': query})


@login_required()
def all_liked_post(request):
    """Выводит все лайкнутые посты пользователя"""
    search_form = SearchForm()
    result = []
    query = None
    if 'query' in request.GET:
        result, query = search(request, 'all_liked_post')
    liked_post = Post.objects.filter(like=request.user.id)
    return render(request, 'registration/liked_post.html', {"liked_post": liked_post, 'result': result,
                                                            'search_form': search_form, 'query': query})


@login_required()
def post_from_subuser(request):
    """Все посты пользователей на которых вы подписаны"""
    search_form = SearchForm()
    result = []
    query = None
    if 'query' in request.GET:
        result, query = search(request, 'post_from_subuser')
    posts = None
    following_ids = request.user.Подписчики.values_list('id', flat=True)
    if following_ids:
        posts = Post.objects.filter(author__in=following_ids, publish=True).order_by('author_id__username')
    return render(request, 'registration/post_from_subuser.html', {'posts': posts, 'result': result,
                                                                   'search_form': search_form, 'query': query})


def action(request):
    """Действия пользователей на которых вы подписаны"""
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.Подписчики.values_list('id', flat=True)  # Получаем подписчиков пользователя
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)  # фильтруем по полученным пользователям
        actions = actions.select_related('user').prefetch_related('target')[:10]
    return render(request, 'registration/action_list.html',
                  {'actions': actions})







# def forgot_password(request):
#     """Views для восстановления забытого пароля"""
#     if request.method == "POST":
#         forgot_form = form.ForgotPasswordForm(request.POST)
#         if forgot_form.is_valid():
#             mail_subject = "Сброс пароля"
#             current_site = get_current_site(request)
#             email = forgot_form.cleaned_data['email']
#             usr = CustomUser.objects.filter(email=email)
#             if len(usr) > 0:
#                 user = usr[0]
#                 user.is_active = False
#                 user.reset_password = True
#                 user.save()
#
#                 message = render_to_string('registration/password_reset_email.html', {
#                     'user': user,
#                     'domain': current_site,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': default_token_generator.make_token(user),
#                     'protocol': 'http',
#                 })
#                 to_email = forgot_form.cleaned_data['email']
#                 email = EmailMessage(mail_subject, message, to=[to_email])
#                 email.send()
#                 return render(request, template_name='registration/password_email_done.html')
#     else:
#         forgot_form = form.ForgotPasswordForm()
#     return render(request, template_name='registration/password_reset_form.html',
#                   context={'forgot_form': forgot_form})
#
#
# def reset(request, uid, token):
#     if request.method == "POST":
#         try:
#             uid = urlsafe_base64_decode(uid).decode()
#             user = CustomUser.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
#             user = None
#
#         if user is not None and password_reset_token.check_token(user, token):
#             reset_form = form.ResetPasswordForm(user=user, data=request.POST)
#             if reset_form.is_valid():
#                 reset_form.save()
#                 update_session_auth_hash(request, reset_form.user)
#
#                 user.is_active = True
#                 user.reset_password = False
#                 # password = reset_form.cleaned_data['password']
#                 # user.set_password(password)
#                 user.save()
#                 return redirect('posts:list')
#     else:
#     # reset_form = form.ResetPasswordForm()
#     # return render(request, template_name='registration/password_reset_form_email.html',
#     #               context={"reset_form": reset_form})
