from django.db import models
from users.models import *
from events.models import *
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='article',
        null=True,
        default=None,
        verbose_name='Категория'
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    positive_grade = models.PositiveIntegerField(
        default=0, verbose_name='Положительные оценки'
    )
    negative_grade = models.IntegerField(
        default=0, verbose_name='Отрицательные оценки'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("article_by_slug", args=[str(self.slug)])

    def save(self, *args, **kwargs):
        title = self.title.lower().replace(' ', '_')
        slug = slugify(unidecode(title))
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True, verbose_name='Адрес страницы'
    )

    def save(self, *args, **kwargs):
        name = self.name.lower().replace(' ', '_')
        slug = slugify(unidecode(name))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return {self.name}

    def get_absolute_url(self):
        return reverse("article_by_category", args=[str(self.slug)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Offer(models.Model):
    STATUS_CHOICES = (
        ('0', 'На модерации'),
        ('1', 'Отклонено'),
        ('2', 'Опубликовано'),
    )
    author = models.ForeignKey(
        'users.Client',
        related_name='offer',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    text = models.TextField(verbose_name='Текст')
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='Статус'
    )

    def __str__(self):
        return {self.text}

    class Meta:
        verbose_name = "Предложение, пожелание"
        verbose_name_plural = "Предложения, пожелания"


class Comment(models.Model):
    STATUS_CHOICES = (
        ('0', 'На модерации'),
        ('1', 'Отклонен'),
        ('2', 'Опубликован'),
    )
    CATEGORY_CHOICES = (
        ('0', 'Общая оценка'),
        ('1', 'Оценка специалиста'),
        ('2', 'Оценка статьи'),
        ('3', 'Оценка тренинга'),
    )
    author = models.ForeignKey(
        'users.Client',
        related_name='comment',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    text = models.TextField(verbose_name='Текст')
    category = models.IntegerField(
        choices=CATEGORY_CHOICES,
        default=0,
        verbose_name='Категория отзыва'
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='Статус'
    )

    def __str__(self):
        return f'{self.category} - {self.text}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Answer(models.Model):
    author = models.ForeignKey(
        'users.MyUser',
        related_name='answer',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    published_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    text = models.TextField(verbose_name='Текст')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    question = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.author.last_name} - {self.text}'

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
