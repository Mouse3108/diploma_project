from django.contrib import admin
from users.models import *
from events.models import *
from information.models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'text', 'category', 'published_date',
        'views', 'positive_grade', 'negative_grade'
    )
    list_display_links = (
        'title', 'text', 'published_date',
        'views', 'positive_grade', 'negative_grade'
    )
    search_fields = ('title', 'text', 'category',)
    list_filter = (
        'category', 'published_date', 'views',
        'positive_grade', 'negative_grade')
    list_editable = ('category',)
    readonly_fields = (
        'published_date', 'views',
        'positive_grade', 'negative_grade'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    readonly_fields = ('slug',)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'published_date', 'author', 'text', 'status'
    )
    list_display_links = (
        'published_date', 'author', 'text'
    )
    search_fields = ('text', 'author',)
    list_filter = ('author', 'published_date')
    list_editable = ('status',)
    readonly_fields = ('published_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'published_date', 'author', 'text',
        'status', 'category'
    )
    list_display_links = ('published_date', 'author', 'text')
    search_fields = ('text', 'author',)
    list_filter = ('author', 'published_date', 'category')
    list_editable = ('status', 'category',)
    readonly_fields = ('published_date',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('published_date', 'author', 'text')
    list_display_links = ('published_date', 'author', 'text')
    search_fields = ('text', 'author',)
    list_filter = ('author', 'published_date')
    readonly_fields = ('published_date',)
