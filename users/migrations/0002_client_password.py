# Generated by Django 5.1.1 on 2024-11-22 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='password',
            field=models.CharField(max_length=100, null=True, verbose_name='Пароль'),
        ),
    ]
