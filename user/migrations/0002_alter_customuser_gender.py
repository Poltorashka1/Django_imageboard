# Generated by Django 4.1.3 on 2022-11-22 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(blank=True, choices=[('мужской', 'Мужской'), ('женский', 'Женский')], default=None, max_length=10, null=True),
        ),
    ]