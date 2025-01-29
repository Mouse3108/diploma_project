from django.contrib import admin
from users.models import *
from events.models import *
from information.models import *
from django.utils.html import format_html


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'time', 'price', 'description', 'status', 'psychologist', 'client'
    )
    list_display_links = (
        'date', 'time', 'description'
    )
    search_fields = ('description',)
    list_filter = ('status', 'date', 'psychologist', 'price',)
    list_editable = ('status', 'psychologist', 'price')


@admin.register(Training)
class Training(admin.ModelAdmin):
    list_display = (
        'date', 'time', 'name', 'status', 'price', 'count_clients', 'clients_for_training'
    )
    list_display_links = (
        'date', 'time', 'name'
    )
    search_fields = ('name',)
    list_filter = ('status', 'count_clients', 'psychologists',)
    list_editable = ('status', 'price', 'count_clients',)
    filter_horizontal = ('psychologists', 'clients',)

    def clients_for_training(self, obj):
        return obj.clients.count()
    clients_for_training.short_description = 'Зарегистрировано участников'

