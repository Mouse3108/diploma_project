from django.db import models
from users.models import *
from information.models import *
from django.core.validators import MaxValueValidator


class Consultation(models.Model):
    STATUS_CHOICES = [
        (0, 'Запланирована'),
        (1, 'Отменена'),
        (2, 'Назначена'),
        (3, 'Проведена'),
    ]
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='Статус')
    psychologist = models.ForeignKey(
        'users.MyUser',
        related_name='psychologist_consultations',
        blank=True,
        null=True,
        verbose_name='Психолог',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        'users.MyUser',
        related_name='client_consultations',
        verbose_name='Клиент',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.date} {self.time} - {self.description}'

    class Meta:
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"


class Training(models.Model):
    STATUS_CHOICES = [
        (0, 'Запланирован'),
        (1, 'Отменен'),
        (2, 'Проведен'),
    ]
    name = models.CharField(max_length=500, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    count_clients = models.PositiveIntegerField(
        verbose_name='Количество участников',
        validators=[MaxValueValidator(20)]
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='Статус')
    psychologists = models.ManyToManyField(
        'users.MyUser',
        verbose_name='Психологи',
        related_name='psychologist_training'
    )
    clients = models.ManyToManyField(
        'users.MyUser',
        verbose_name='Клиенты',
        related_name='client_training'
    )

    def __str__(self):
        return f'{self.date} {self.time} - {self.name}'

    class Meta:
        verbose_name = "Тренинг"
        verbose_name_plural = "Тренинги"
