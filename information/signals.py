from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from events.models import *
from users.models import *
from .telegram_bot import send_telegram_message
from harmony.settings import TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID
import asyncio


@receiver(post_save, sender=Consultation)
def send_consultation_notification(sender, instance, created, **kwargs):
    if not created:
        if instance.status == 2:
            message = f"""
    *У нас новая запись на консультацию!*

    *Дата консультации:* {instance.date.strftime('%d.%m.%Y')}
    *Время консультации:* {instance.time.strftime('%H:%M')}
    *Психолог:* {instance.psychologist.first_name} {instance.psychologist.last_name}
    
    *Клиент:* {instance.client.first_name} {instance.client.last_name}
    *Телефон:* {instance.client.phone}
    *Описание проблемы:* {instance.description}

    *Подробнее:* http://127.0.0.1:8000/admin/information/consultation/{instance.id}/change/
    """
            asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))

        elif instance.status == 1:
            message = f"""
    *Клиент отменил свою запись на консультацию!*

    *Дата консультации:* {instance.date.strftime('%d.%m.%Y')}
    *Время консультации:* {instance.time.strftime('%H:%M')}
    *Психолог:* {instance.psychologist.first_name} {instance.psychologist.last_name}
    
    *Клиент:* {instance.client.first_name} {instance.client.last_name}
    *Телефон:* {instance.client.phone}

    *Подробнее:* http://127.0.0.1:8000/admin/information/consultation/{instance.id}/change/
    """
            asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))


@receiver(m2m_changed, sender=Training.clients.through)
def send_client_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        new_clients = MyUser.objects.filter(pk__in=pk_set)
        for client in new_clients:
            message = f"""
*К нам на тренинг зарегистрировался новый клиент!*

*Тренинг:* {instance.name}
*Дата тренинга:* {instance.date.strftime('%d.%m.%Y')}
*Время начала тренинга:* {instance.time.strftime('%H:%M')}

*Клиент:* {client.first_name} {client.last_name}
*Телефон:* {client.phone}

*Подробнее:* http://127.0.0.1:8000/admin/information/training/{instance.id}/change/
"""
            asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))

    elif action == "post_remove":
        removed_clients = MyUser.objects.filter(pk__in=pk_set)
        for client in removed_clients:
            message = f"""
*Один из наших клиентов передумал участвовать в тренинге!*

*Тренинг:* {instance.name}
*Дата тренинга:* {instance.date.strftime('%d.%m.%Y')}

*Клиент:* {client.first_name} {client.last_name}
*Телефон:* {client.phone}

*Подробнее:* http://127.0.0.1:8000/admin/information/training/{instance.id}/change/
"""
            asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, YOUR_PERSONAL_CHAT_ID, message))

