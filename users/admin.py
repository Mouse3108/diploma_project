from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import *
from events.models import *
from information.models import *
from django.utils.html import format_html


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'display_photo', 'first_name', 'last_name',
        'job_title', 'phone', 'email',
        'all_consultations', 'all_trainings'
    )
    list_display_links = (
        'display_photo', 'first_name', 'last_name',
        'job_title', 'phone', 'email'
    )
    list_filter = ('job_title',)
    readonly_fields = ('show_photo',)

    def display_photo(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" />', obj.avatar.url
            )
        else:
            return "-"
    display_photo.short_description = 'Фото'

    def show_photo(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="200" />', obj.avatar.url
            )
        else:
            return "-"
    show_photo.short_description = 'Фото'

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('show_photo', 'avatar', 'job_title', 'phone')}),
    )

    def all_consultations(self, obj):
        return Consultation.objects.filter(psychologist=obj, status=3).count()
    all_consultations.short_description = 'Проведено консультаций'

    def all_trainings(self, obj):
        return Training.objects.filter(psychologists=obj, status=2).count()
    all_trainings.short_description = 'Проведено тренингов'


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        'display_photo', 'educational_institution', 'status',
        'speciality', 'year', 'psychologist'
    )
    list_display_links = (
        'display_photo', 'educational_institution',
        'speciality', 'year'
    )
    search_fields = ('educational_institution', 'speciality')
    list_filter = (
        'psychologist', 'educational_institution',
        'status', 'speciality',
    )
    list_editable = ('status', 'psychologist',)
    readonly_fields = ('show_photo',)

    def display_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" />', obj.photo.url
            )
        else:
            return "-"
    display_photo.short_description = 'Диплом или сертификат'

    def show_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" />', obj.photo.url
            )
        else:
            return "-"
    show_photo.short_description = 'Диплом или сертификат'

    fieldsets = (
        (None, {
            'fields': (
                'educational_institution',
                'status',
                'speciality',
                'year',
                'show_photo',
                'photo'
            )
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'display_photo', 'username', 'first_name', 'last_name',
        'date_birth', 'email', 'phone'
    )
    list_display_links = (
        'display_photo', 'username', 'first_name', 'last_name',
        'date_birth', 'email', 'phone'
    )
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('date_birth', 'first_name', 'last_name',)
    readonly_fields = ('show_photo',)

    def display_photo(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" />', obj.avatar.url
            )
        else:
            return "-"
    display_photo.short_description = 'Аватар'

    def show_photo(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="200" />', obj.avatar.url
            )
        else:
            return "-"
    show_photo.short_description = 'Аватар'

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password',
                'first_name',
                'last_name',
                'date_birth',
                'email',
                'phone',
                'show_photo',
                'avatar'
            )
        }),
    )
