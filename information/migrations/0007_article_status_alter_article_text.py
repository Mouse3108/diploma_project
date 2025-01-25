# Generated by Django 5.1.1 on 2025-01-24 06:56

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_alter_comment_answer_alter_offer_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(1, 'Опубликовано'), (0, 'Черновик')], default=0, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=tinymce.models.HTMLField(verbose_name='Текст'),
        ),
    ]
