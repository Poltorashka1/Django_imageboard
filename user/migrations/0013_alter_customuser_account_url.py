# Generated by Django 4.1.3 on 2022-12-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='account_url',
            field=models.SlugField(blank=True, max_length=30, null=True, unique=True, verbose_name='Ссылка'),
        ),
    ]
