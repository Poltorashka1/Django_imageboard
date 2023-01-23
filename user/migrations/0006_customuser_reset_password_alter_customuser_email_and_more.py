# Generated by Django 4.1.3 on 2022-11-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='reset_password',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('мужской', 'Мужской'), ('женский', 'Женский')], default=None, max_length=10, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='telegram',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Telegram'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Возраст'),
        ),
    ]
