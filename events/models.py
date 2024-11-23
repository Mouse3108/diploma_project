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
        related_name='consultations',
        verbose_name='Психолог',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        'users.Client',
        related_name='consultations',
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
        verbose_name='Психологи'
    )
    clients = models.ManyToManyField(
        'users.Client',
        verbose_name='Клиенты'
    )

    def __str__(self):
        return f'{self.date} {self.time} - {self.name}'

    class Meta:
        verbose_name = "Тренинг"
        verbose_name_plural = "Тренинги"


class TrainingsPhoto(models.Model):
    photo = models.ImageField(
        upload_to='trainings photo',
        verbose_name=''
    )
    training = models.ForeignKey(
        'Training',
        related_name='trainings_photo',
        verbose_name='Тренинг',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Фото тренинга"
        verbose_name_plural = "Фото тренингов"
