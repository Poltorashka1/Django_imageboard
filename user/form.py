from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm as Ps
from captcha.fields import CaptchaField

CustomUser = get_user_model()


class UserLoginForm(forms.Form):
    """Форма для входа пользователя """
    username = forms.CharField(max_length=128, label="Имя/Почта")
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    captcha = CaptchaField(label='Капча')
    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if models.CustomUser.objects.filter(username=username).exists() or models.CustomUser.objects.filter(
    #             email=username).exists():
    #         return username
    #     else:
    #         raise ValidationError('Неверный логин или пароль')


class UserInfoChangeForm(forms.ModelForm):
    """ Форма для редактирования информации о пользователе """
    # Показывает поле немного в другом формате и не дает редактировать
    email = forms.EmailField(disabled=True, label='Почта')
    captcha = CaptchaField(label='Капча')
    # Оставляет поле но не дает его редактировать
    # def __init__(self, *args, **kwargs):
    #     super(UserInfoChangeForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['readonly'] = True

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'year', 'telegram', 'gender', 'account_url', 'image')

    def clean_year(self):
        cd = self.cleaned_data
        year = cd['year']
        if 'year' in self.changed_data and year != None:
            if year < 16:
                raise ValidationError("Возраст должен быть больше 15 лет")
        return year

    def clean_username(self):
        username = self.cleaned_data['username']
        if 'username' in self.changed_data:
            if models.CustomUser.objects.filter(username=username).exists():
                raise ValidationError('Пользователь с таким именем уже существует')
        return username

    def clean_account_url(self):
        account_url = self.cleaned_data['account_url']
        if 'account_url' in self.changed_data:
            if models.CustomUser.objects.filter(account_url=account_url).exists():
                raise ValidationError('Пользователь с такой ссылкой уже существует')
        return account_url


class UserRegisterForm(forms.ModelForm):
    """Форма для регистрации пользователя"""
    # Посмотреть UserCreationForm
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    email = forms.EmailField(label="Почта", max_length=200, required=True)
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def clean_password2(self):
        cd = self.cleaned_data
        if len(cd['password2']) < 8:
            raise ValidationError('Пароль должен быть длиннее 8 символов')
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Почта уже используется')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if models.CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username


class PasswordResetForm(Ps):
    """Расширяем стандартную форму добавляя в нее проверку на наличие почты"""

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.CustomUser.objects.filter(email=email).exists():
            return email
        raise ValidationError("Такой почты не существует")

# Пока не работает
# class ForgotPasswordForm(forms.Form):
#     """Восстановление пароля"""
#     email = forms.EmailField(label="Почта", required=True, max_length=50)
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         if models.CustomUser.objects.filter(email=email).exists():
#             return email
#         raise ValidationError("Такой почты не существует")
# class ResetPasswordForm(forms.ModelForm):
#     """Не используется"""
#     password = forms.CharField(widget=forms.PasswordInput, label='Новый пароль')
#     password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
#
#     class Meta:
#         model = CustomUser
#         fields = ('password',)
#
#     def clean_password2(self):
#         password = self.cleaned_data['password']
#         password2 = self.cleaned_data['password2']
#         if password != password2:
#             raise ValidationError("Пароли не совпадают")
#         return password2
