# Generated by Django 5.1.1 on 2024-11-22 09:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('status', models.IntegerField(choices=[(0, 'Запланирована'), (1, 'Отменена'), (2, 'Назначена'), (3, 'Проведена')], default=0, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Консультация',
                'verbose_name_plural': 'Консультации',
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('count_clients', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(20)], verbose_name='Количество участников')),
                ('status', models.IntegerField(choices=[(0, 'Запланирован'), (1, 'Отменен'), (2, 'Проведен')], default=0, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Тренинг',
                'verbose_name_plural': 'Тренинги',
            },
        ),
        migrations.CreateModel(
            name='TrainingsPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='trainings photo', verbose_name='')),
            ],
            options={
                'verbose_name': 'Фото тренинга',
                'verbose_name_plural': 'Фото тренингов',
            },
        ),
    ]