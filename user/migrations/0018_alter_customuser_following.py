# Generated by Django 4.1.3 on 2023-01-13 19:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_contact_customuser_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='user.Contact', to=settings.AUTH_USER_MODEL),
        ),
    ]
