import datetime
from urllib import request

from django import forms
from django.forms import ValidationError
from slugify import slugify
from captcha.fields import CaptchaField

from . import models


def check_image_from_format(self):
    if self.cleaned_data['image']:
        image = self.cleaned_data['image']
        valid = ['jpg', 'jpeg']
        if image.name.rsplit('.', 1)[1].lower() not in valid:
            raise ValidationError('Фотография должна быть jpg или jpeg')
        return image
    return None


class CommentCreateForm(forms.ModelForm):
    # captcha = CaptchaField(label='Капча')
    replyy = forms.IntegerField(label="Ответить", required=False)

    class Meta:
        model = models.Comment
        fields = ('replyy', 'text', 'image',)

    def clean_image(self):
        return check_image_from_format(self)


class PostCreationForm(forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = models.Post
        fields = ('name', 'text', 'board', 'image')

    def clean_slug(self):
        name = self.cleaned_data['name']
        text = self.cleaned_data['text']
        slug = name + text[:10]
        if models.Post.objects.filter(slug=slug).exists():
            raise ValidationError("Поменяйте название или отредактируйте начало текста")
        return slug

    def clean_image(self):
        return check_image_from_format(self)


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, label='Поиск')
