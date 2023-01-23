import random

from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.urls import reverse
from slugify import slugify


# Create your models here.
class CustomUser(AbstractUser):
    """Расширенный пользователь"""
    GENDER_CHOICES = (('мужской', 'Мужской'), ('женский', 'Женский'))
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='Почта')
    year = models.IntegerField(blank=True, null=True, verbose_name='Возраст')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None, blank=True, null=True,
                              verbose_name='Пол')
    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telegram')
    account_url = models.SlugField(max_length=30, null=True, blank=True, verbose_name="Ссылка", unique=True)
    email_confirm = models.BooleanField(default=False, verbose_name='Пользователь подтвердил почту')
    image = models.ImageField(upload_to='images/user_photo/', blank=True, null=True, verbose_name="Картинка")
    following = models.ManyToManyField('self', through="Contact", related_name='Подписчики', symmetrical=False)

    # reset_password = models.BooleanField(default=False, verbose_name='Пользователь меняет пароль')
    class Meta:
        permissions = [
            ('administrator', 'Check_post_comments')
        ]

    def save(self, *args, **kwargs):
        if not self.account_url:
            self.account_url = slugify(self.username) + str(random.randint(10000000, 10000000000000))
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:user_profile', args=[self.account_url])


class Contact(models.Model):
    sub_user = models.ForeignKey('CustomUser', related_name='sub_user', on_delete=models.CASCADE)
    user_to_sub = models.ForeignKey('CustomUser', related_name='user_to_sub', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_to_sub} подписался на {self.sub_user}"

