from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import reverse
from slugify import slugify

# Create your models here.
CustomUser = get_user_model()


class PublishedPostManager(models.Manager):
    """Менеджер модели Post"""

    def get_queryset(self):
        return super().get_queryset().filter(publish=True).annotate(like_count=Count('like')).order_by('-like_count')


class Board(models.Model):
    name = models.CharField(max_length=125, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    slug = models.SlugField(unique=True, verbose_name="Slug", blank=True, null=True)

    # To do для редакторов
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name, allow_unicode=True)
    #     super(Board, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts:list', args=[self.slug])


class Post(models.Model):
    """Модель постов"""
    name = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=250, unique=True, verbose_name="Slug")
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_author', verbose_name="Автор", )
    publish = models.BooleanField(default=False, verbose_name="Видимость")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board', verbose_name='Доска', blank=True,
                              null=True)
    image = models.ImageField(upload_to='images/posts/', blank=True, null=True, verbose_name='Картинка')
    like = models.ManyToManyField(CustomUser, related_name='Лайки', blank=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.name}-{self.text[:10]}")  # allow_unicode позволяет сохранять русские буквы, но если мы в юрл указываем <slug:slug> то оно работать не будет
            # Используем библиотеку для автоматического перевода слага из ру в англ
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.slug, self.pk])

    objects = models.Manager()
    published = PublishedPostManager()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Название поста')
    text = models.TextField(verbose_name="Комментарий")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author', verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    active = models.BooleanField(default=True, verbose_name='Видимость')
    image = models.ImageField(upload_to='images/comments/', blank=True, null=True, verbose_name='Картинка')
    reply = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reply_comment')
    # Не удаляет фото при редактировании поста

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text[:10]
