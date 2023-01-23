from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.postgres.search import SearchVector
from actions.utils import create_action

from . import form
from . import models


# Create your views here.

def pagination(request, query, obj: int):
    """Пагинация"""
    paginator = Paginator(query, obj)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return posts


def post_list(request, board=None):
    """Список всех постов, или постов определенной доски"""
    search_form = form.SearchForm()
    query = None
    result = []
    if 'query' in request.GET:
        result, query = search(request.GET)

    all_board = models.Board.objects.all()
    all_post = models.Post.published.all()
    board_name = 'Главная страница'
    if board:
        all_post = models.Post.published.filter(board__slug=board)
        board_name = get_object_or_404(models.Board, slug=board)
    posts = pagination(request, all_post, 6)
    return render(request, template_name='post/post_list.html',
                  context={'posts': posts, "all_board": all_board, 'board_name': board_name, 'result': result,
                           'search_form': search_form, 'query': query})


def search(param):
    """Функция для поиска"""
    search_form = form.SearchForm(param)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        result = models.Post.published.annotate(search=SearchVector('text', 'name', 'author_id__username'), ).filter(
            search=query)
        if len(result) == 0:
            return result, False
        else:
            return result, True
    return None


@login_required
def post_like(request, pk, action):
    """Лайк для поста"""
    post = get_object_or_404(models.Post, pk=pk)
    if action:
        try:
            if action == "like":
                post.like.add(request.user)
                create_action(request.user, f"Оценил пост", post)
            if action == 'unlike':
                post.like.remove(request.user)
        except:
            pass
    return redirect('posts:post_detail', slug=post.slug, pk=post.pk)


@login_required
def post_detail(request, slug, pk, comment_id=None):
    """Вся информация для каждого поста"""
    detail_post = get_object_or_404(models.Post, slug=slug, pk=pk, publish=True)
    if request.method == "POST":
        comment_form = form.CommentCreateForm(data=request.POST, files=request.FILES)
        if comment_form.is_valid():
            parent = None
            try:
                parent_id = int(request.POST.get('replyy'))
            except:
                parent_id = None
            if parent_id:
                parent = models.Comment.objects.get(id=parent_id)
                if parent:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.author = request.user
                    reply_comment.reply = parent
                    reply_comment.post = detail_post
                    reply_comment.save()
                    return HttpResponseRedirect(request.path)
            else:
                new_comment = comment_form.save(commit=False)
                new_comment.post = detail_post
                new_comment.author = request.user
                new_comment.save()
                return HttpResponseRedirect(request.path)
    else:
        comment_form = form.CommentCreateForm()
    all_comment = models.Comment.objects.filter(post=detail_post, active=True, reply__isnull=True)
    comments = pagination(request, all_comment, 5)
    # if request.user == detail_post.author:
    #     edit = True
    # else:
    #     edit = False
    all_user_like = detail_post.like.all()
    return render(request, template_name='post/post_detail.html',
                  context={'detail_post': detail_post, "comment_form": comment_form, 'comments': comments,
                           'all_comment': all_comment, 'author_like': all_user_like})


@login_required
@permission_required('user.administrator')
def post_edit(request, slug):
    """Редактирование поста"""
    post = get_object_or_404(models.Post, slug=slug)
    if request.user == post.author:
        if request.method == 'POST':
            post_form = form.PostCreationForm(data=request.POST, instance=post, files=request.FILES)
            if post_form.is_valid():
                post_form.save()
            return redirect('posts:post_detail', slug=post.slug, pk=post.pk)
        else:
            post_form = form.PostCreationForm(instance=post)
        return render(request, template_name='post/post_creation.html', context={'post_form': post_form})
    else:
        return redirect('posts:list')


@login_required
def new_post(request):
    """Создание нового поста"""
    if request.method == "POST":
        post_form = form.PostCreationForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_new = post_form.save(commit=False)
            post_new.author = request.user
            post_new.save()
            create_action(request.user, 'Создал пост', post_new)
            return render(request, template_name='post/check_post.html')
    else:
        post_form = form.PostCreationForm()
    return render(request, template_name='post/post_creation.html', context={'post_form': post_form})


# To Do поиск и выбор сортировки

def sort(request, sort):
    pass

# def search(request):
#     query = None
#     result = []
#     if 'query' in request.GET:
#         search_form = form.SearchForm(request.GET)
#         if search_form.is_valid():
#             query = search_form.cleaned_data['query']
#             result = models.Post.objects.annotate(search=SearchVector('name', 'text'), ).filter(search=query)
#     return render(request, 'post/search.html',
#                   context={"result": result, 'search_form': search_form, 'query': query})
# def get_most_commented_posts(count=5):
# return Post.published.annotate(total_comments=Count('comments'))
# .order_by('-total_comments')[:count]
