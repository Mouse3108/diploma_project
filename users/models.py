from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models
from tinymce.models import HTMLField


class MyUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/users',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )
    date_birth = models.DateField(
        blank=True,
        null=True,
        default=None,
        verbose_name='Дата рождения'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Телефон'
    )
    job_title = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Должность'
    )
    job_speciality = HTMLField(
        blank=True,
        null=True,
        verbose_name='Направления работы'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Education(models.Model):
    STATUS_CHOICES = [
        (1, 'Высшее образование'),
        (2, 'Повышение квалификации'),
        (3, 'Семинар'),
        (4, 'Обучающий курс'),
        (0, 'Другое'),
    ]
    educational_institution = models.CharField(
        max_length=200,
        verbose_name='Учебное заведение'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
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
        'users.MyUser',
        on_delete=models.CASCADE,
        related_name='psychologist',
        verbose_name='Психолог'
    )

    def __str__(self):
        return f'{self.educational_institution} ({self.status}) - {self.year}'

    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образование"



