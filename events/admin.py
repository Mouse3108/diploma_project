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
