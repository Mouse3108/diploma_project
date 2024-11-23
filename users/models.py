from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db import models


class MyUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/users',
        blank=True,
        null=True,
        verbose_name=''
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    job_title = models.CharField(
        max_length=50,
        verbose_name='Должность'
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Education(models.Model):
    STATUS_CHOICES = [
        ('ВУЗ', 'Высшее образование'),
        ('ПК', 'Повышение квалификации'),
        ('С', 'Семинар'),
        ('ОК', 'Обучающий курс'),
        ('Д', 'Другое'),
    ]
    educational_institution = models.CharField(
        max_length=200,
        verbose_name='Учебное заведение'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default='Д',
        verbose_name='Статус'
    )
    speciality = models.TextField(
        verbose_name='Специальность'
    )
    year = models.CharField(
        max_length=4,
        verbose_name='Год окончания'
    )
    photo = models.ImageField(
        upload_to='diplomes/',
        blank=True,
        null=True,
        verbose_name=''
    )
    psychologist = models.ForeignKey(
        'MyUser',
        on_delete=models.CASCADE,
        related_name='psychologist',
        verbose_name='Психолог'
    )

    def __str__(self):
        return f'{self.educational_institution} ({self.status}) - {self.year}'

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"


class Client(AbstractBaseUser):
    avatar = models.ImageField(
        upload_to='avatars/clients',
        blank=True,
        null=True,
        verbose_name=''
    )
    username = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Ник'
    )
    password = models.CharField(
        max_length=100,
        verbose_name='Пароль'
    )
    first_name = models.CharField(
        max_length=50,
        null=True,
        default=None,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=200,
        null=True,
        default=None,
        verbose_name='Фамилия'
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Дата рождения'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email'
    )
    phone = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
