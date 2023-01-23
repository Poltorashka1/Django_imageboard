from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from . import form

# Register your models here.

CustomUser = get_user_model()


# class CustomUserAdmin(UserAdmin):
#     add_form = form.CustomUserCreationForm
#     form = form.CustomUserChangeForm
#     model = CustomUser
#     UserAdmin.list_display = ['username']
#     # Добавляет поля в начало
#     fields = list(UserAdmin.fieldsets)
#     fields[0] = (None, {'fields': ('username', 'password', 'year', 'telegram', 'gender')})
#     UserAdmin.fieldsets = tuple(fields)
#
#     # Добавляет поля в конец
#     # UserAdmin.fieldsets = (*UserAdmin.fieldsets,('Other Personal info',{'fields': ('year', 'gender', 'telegram',)}))
#
@admin.register(CustomUser)
class CustomModelAdmin(UserAdmin):
    list_display = ('username', 'email', 'pk', 'image')
    ordering = ('-username',)

    # Добавляет поля в начало не работает
    # fields = list(UserAdmin.fieldsets)
    # fields[0] = (None, {'fields': ('username', 'password', 'year', 'telegram', 'gender', 'reset_password', 'email_confirm')})
    # fieldsets = tuple(fields)

    # Добавление полей в начало
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CustomModelAdmin, self).get_fieldsets(request, obj)
        new_fieldsets = list(fieldsets)
        new_fieldsets[0] = (
            None,
            {'fields': ('username', 'password', 'year', 'telegram', 'gender', 'email_confirm', 'account_url',
                        'image',)})  # Не дает возможность добавить following
        return new_fieldsets

    # Добавление полей в конец
    # def get_fieldsets(self, request, obj=None):
    #     fieldsets = super(CustomModelAdmin, self).get_fieldsets(request, obj)
    #     new_fieldsets = list(fieldsets)
    #     new_fieldsets.append(["Информация о пользователе", {
    #         'fields': ('year', 'telegram', 'gender', 'reset_password', 'email_confirm')}])
    #     return new_fieldsets

    # Добавляет поля в конец
    # UserAdmin.fieldsets = (*UserAdmin.fieldsets,('Other Personal info',{'fields': ('year', 'gender', 'telegram',)}))
