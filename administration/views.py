from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from posts.models import Post, Board, Comment
from user.models import CustomUser
from posts.views import pagination
from django.http import HttpResponse
from . import form
from posts import models
from django.contrib.postgres.search import SearchVector


# Create your views here.
@permission_required('user.administrator')
@login_required
def all_func_view(request):
    """Отображение всех возможностей"""
    return render(request, template_name='administration/all_func.html')


@permission_required('user.administrator')
def all_unverified_post(request):
    """Список всех непроверенных постов"""
    search_form = form.Search()
    result = []
    query = None
    if 'search' in request.GET:
        result, query = search(request.GET, "black")

    unpublish = Post.objects.filter(publish=False)
    return render(request, template_name='administration/check_unverified_post.html',
                  context={'unpublish': unpublish, 'search_form': search_form, 'result': result,
                           'query': query})


# def new_search(param):
#     search_form = form.Search(param)
#     if search_form.is_valid():
#         search = search_form.cleaned_data['search']
#         result = models.Post.objects.annotate(search=SearchVector('text', 'name', 'author_id__username'), ).filter(
#             search=search, publish=False)
#         if len(result) == 0:
#             return result, False
#         else:
#             return result, True
#     return None


@permission_required('user.administrator')
def decision(request, pk, slug, action):
    """Публикация или удаление поста"""
    post = Post.objects.filter(pk=pk, slug=slug)
    if action == 'accept':
        post.update(publish=True)
    if action == 'delete':
        return render(request, template_name='administration/post_delete.html', context={'pk': pk, "slug": slug})
    if action == 'delete_true':
        post.delete()
        return redirect('administration:all_post')
    if action == 'delete_false':
        return redirect("administration:all_post")
    else:
        pass
    return redirect('administration:check_post')


@permission_required('user.administrator')
def delete_comment(request, pk, action, slug, post_pk):
    comment = Comment.objects.filter(pk=pk)
    if action == 'delete':
        comment.delete()
    return redirect('posts:post_detail', slug=slug, pk=post_pk)


@permission_required('user.administrator')
def all_post(request, board=None):
    """Все посты независимо от публикации"""
    search_form = form.Search()
    query = None
    result = []
    if 'search' in request.GET:
        result, query = search(request.GET, "white")

    posts = Post.objects.all()
    all_board = Board.objects.all()
    if board:
        posts = Post.objects.filter(board__slug=board)
    posts = pagination(request, posts, 6)
    return render(request, template_name='administration/all_post.html',
                  context={'posts': posts, 'all_board': all_board, 'result': result, 'query': query,
                           'search_form': search_form})


@permission_required('user.administrator')
def check_user(request):
    search_form = form.Search()
    result = []
    query = None
    if 'search' in request.GET:
        result, query = search(request.GET, 'user')

    all_user = CustomUser.objects.all()
    return render(request, template_name='administration/all_user.html',
                  context={"all_user": all_user, 'result': result, 'query': query,
                           'search_form': search_form})


@permission_required('user.administrator')
def deactive_user(request, username, pk, action):
    user = CustomUser.objects.filter(username=username, pk=pk)
    if action == 'deactivate':
        user.update(is_active=False)
    if action == 'active':
        user.update(is_active=True)
    else:
        pass
    return redirect('administration:check_user')


def search(param, section):
    search_form = form.Search(param)
    if search_form.is_valid():
        search = search_form.cleaned_data['search']

        if section == 'white':
            result = models.Post.published.annotate(
                search=SearchVector('text', 'name', 'author_id__username'), ).filter(
                search=search)
        elif section == 'black':
            result = models.Post.objects.annotate(search=SearchVector('text', 'author_id__username', 'name'), ).filter(
                search=search, publish=False)
        elif section == 'user':
            result = models.CustomUser.objects.annotate(search=SearchVector('username'), ).filter(search=search)
        else:
            result = None

        if len(result) == 0:
            return result, False
        else:
            return result, True
    return None
