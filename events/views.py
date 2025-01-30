from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from .models import *
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.views.generic.edit import FormMixin
import json
from django.utils.http import urlencode
from urllib.parse import unquote
from django.utils.decorators import method_decorator
from datetime import datetime, date
from django.utils import timezone
from .forms import *
from django.db.models import Q


menu = [
    {"title": "Главная", "alias": "main", "icon": "bi-house"},
    {"title": "Наши специалисты", "alias": "users:specialists", "icon": "bi-person"},
    {"title": "Советы психолога", "alias": "information:articles", "icon": "bi-chat-dots"},
    {"title": "Тестирование", "alias": "tests:testing", "icon": "bi-ui-checks-grid"},
    {"title": "Консультации", "alias": "events:consultations", "icon": "bi-clipboard"},
    {"title": "Тренинги", "alias": "events:trainings", "icon": "bi-briefcase"},
    {"title": "Отзывы клиентов", "alias": "information:comments", "icon": "bi-list-stars"},
    {"title": "Ваши предложения", "alias": "information:offers", "icon": "bi-lightbulb"}
]


class ConsultationsView(ListView):
    model = Consultation
    template_name = 'consultation/consultations.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            now = timezone.localtime(timezone.now())
            today = now.date()
            current_time = now.time()
            if self.request.user.is_staff:
                return (Consultation.objects.select_related('psychologist').
                        filter(Q(date__gt=today) | Q(date=today, time__gt=current_time)).
                        filter(psychologist=self.request.user).
                        order_by('date', 'time'))
            else:
                return (Consultation.objects.select_related('psychologist').
                        filter(Q(date__gt=today) | Q(date=today, time__gt=current_time), status=0).
                        order_by('date', 'time'))
        else:
            return Consultation.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consultations = self.get_queryset()
        context['menu'] = menu
        context['page_alias'] = 'events:consultations'
        dates = set(consultation.date for consultation in consultations)
        context['dates'] = sorted(dates)
        psychologists = set(consultation.psychologist for consultation in consultations)
        context['psychologists'] = psychologists
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
        return context


class UpdateConsultationClientView(LoginRequiredMixin, UpdateView):
    model = Consultation
    form_class = ConsultationUpdateForm
    template_name = 'consultation/update_consultation_client.html'
    success_url = reverse_lazy('events:consultations')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'events:consultations'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.user_has_consultation_today(request.user, self.object.date):
            messages.error(request, "У вас уже есть запись на консультацию в этот день."
                                    "Выберите другую дату")
            return redirect(self.success_url)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def user_has_consultation_today(self, client, date):
        return Consultation.objects.filter(client=client, date=date).exists()

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно записались на консультацию")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class ClientConsultationView(ListView):
    model = Consultation
    template_name = 'client/consultation_client.html'
    context_object_name = 'client_consultations'

    def get_queryset(self):
        return (Consultation.objects.filter(client=self.request.user).
                select_related('psychologist').order_by('-date', '-time'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:client_consultations'
        return context


class CancelConsultationClientView(LoginRequiredMixin, View):
    def get_success_url(self):
        return reverse_lazy('users:client_consultations', kwargs={'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        consultation = get_object_or_404(Consultation, pk=kwargs['pk'])
        consultation.status = 1
        consultation.save()
        Consultation.objects.create(
            psychologist=consultation.psychologist,
            date=consultation.date,
            time=consultation.time,
            price=consultation.price
        )
        messages.success(request, "Консультация отменена. "
                                  "Но Вы в любой момент можете записаться на новую консультацию")
        return redirect(self.get_success_url())


class TrainingsView(ListView):
    model = Training
    template_name = 'training/trainings.html'
    context_object_name = 'trainings'

    def get_queryset(self):
        now = timezone.localtime(timezone.now())
        today = now.date()
        current_time = now.time()
        if self.request.user and self.request.user.is_staff:
            return (Training.objects.prefetch_related('psychologists', 'clients').
                    filter(Q(date__gt=today) | Q(date=today, time__gt=current_time)).
                    filter(psychologists=self.request.user).
                    order_by('date', 'time'))
        else:
            return (Training.objects.prefetch_related('psychologists', 'clients').
                    filter(Q(date__gt=today) | Q(date=today, time__gt=current_time)).
                    filter(status=0).order_by('date', 'time'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'events:trainings'
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
        return context


class UpdateTrainingClientView(LoginRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingUpdateForm
    template_name = 'training/update_training_client.html'
    success_url = reverse_lazy('events:trainings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        kwargs['training'] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'events:trainings'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.user_has_training(self.object.id):
            messages.error(request, "Вы уже зарегистрировались на этот тренинг")
            return redirect(self.success_url)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def user_has_training(self, id):
        return Training.objects.filter(id=id, clients__in=[self.request.user]).exists()

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно зарегистрировались на участие в тренинге")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class CancelTrainingClientView(LoginRequiredMixin, View):
    def get_success_url(self):
        return reverse_lazy('users:client_trainings', kwargs={'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        training = get_object_or_404(Training, pk=kwargs['pk'])
        training.clients.remove(request.user)
        training.save()
        messages.success(request, "Ваше участие в тренинге отменено. "
                                  "Но Вы в любой момент можете зарегистрироваться на другое мероприятие")
        return redirect(self.get_success_url())


class ClientTrainingView(ListView):
    model = Training
    template_name = 'client/training_client.html'
    context_object_name = 'client_trainings'

    def get_queryset(self):
        return (Training.objects.prefetch_related('psychologists', 'clients').
                filter(clients=self.request.user).order_by('-date', '-time'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:client_trainings'
        return context
