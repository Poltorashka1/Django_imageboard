from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
CustomUser = get_user_model()


@admin.register(models.Post)
class Post(admin.ModelAdmin):
    list_display = ('name', 'publish', 'pk')
    prepopulated_fields = {"slug": ('name',)}

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(Post, self).get_fieldsets(request, obj)
        new_fieldsets = list(fieldsets)
        new_fieldsets[0] = (
            None, {'fields': ('name', 'slug', 'text', 'author', 'publish', 'board', 'image', 'like')})
        return new_fieldsets


@admin.register(models.Board)
class Board(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Comment)
class Comments(admin.ModelAdmin):
    list('text')
