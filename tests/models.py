from django.db import models
from users.models import *
from tinymce.models import HTMLField


class TestResults(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название теста'
    )
    testing_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата тестирования'
    )
    client = models.ForeignKey(
        'users.MyUser',
        related_name='test',
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    balls = models.IntegerField(
        verbose_name='Набранные балы'
    )
    result = models.CharField(
        max_length=200,
        verbose_name='Результат'
    )

    def __str__(self):
        return f'{self.testing_date} - {self.name}'

    class Meta:
        verbose_name = 'Тестирование пользователя'
        verbose_name_plural = 'Тестирование пользователей'


class FunnyTest(models.Model):
    question = HTMLField(
        verbose_name='Вопрос'
    )
    answer1 = models.CharField(
        max_length=200,
        verbose_name='Ответ № 1'
    )
    answer2 = models.CharField(
        max_length=200,
        verbose_name='Ответ № 2'
    )
    correct_answer = models.CharField(
        max_length=200,
        verbose_name='Правильный ответ'
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Тест-шутка'


class FunnyTestResult(models.Model):
    min_balls = models.IntegerField(
        verbose_name='Минимальный бал'
    )
    max_balls = models.IntegerField(
        verbose_name='Максимальный бал'
    )
    result = HTMLField(
        verbose_name='Результат'
    )

    def __str__(self):
        return f'{self.min_balls}-{self.max_balls}: {self.result}'

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Результаты теста-шутки'

