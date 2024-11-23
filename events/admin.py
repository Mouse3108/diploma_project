from django.contrib import admin
from users.models import *
from events.models import *
from information.models import *
from django.utils.html import format_html


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'time', 'description', 'status'
    )
    list_display_links = (
        'date', 'time', 'description'
    )
    search_fields = ('description',)
    list_filter = ('status', 'date',)
    list_editable = ('status',)


@admin.register(Training)
class Training(admin.ModelAdmin):
    list_display = (
        'date', 'time', 'name', 'description',
        'status', 'count_clients'
    )
    list_display_links = (
        'date', 'time', 'name',
        'description', 'count_clients'
    )
    search_fields = ('description', 'name', 'status',)
    list_filter = ('status', 'date',)
    list_editable = ('status',)
    filter_horizontal = ('psychologists', 'clients',)


@admin.register(TrainingsPhoto)
class TrainingsPhotoAdmin(admin.ModelAdmin):
    list_display = ('display_photo', 'training')
    search_fields = ('training_name',)
    readonly_fields = ('show_photo',)

    def display_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" />', obj.photo.url
            )
        else:
            return "-"
    display_photo.short_description = 'Аватар'

    def show_photo(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" />', obj.photo.url
            )
        else:
            return "-"
    show_photo.short_description = 'Аватар'

    fieldsets = ((None,
                  {'fields': ('show_photo', 'photo')}
                  ),)
