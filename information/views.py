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
from .forms import *
# import json
from django.utils.http import urlencode
from urllib.parse import unquote


menu = [
    {"title": "Главная", "alias": "main", "icon": "bi-house"},
    {"title": "Наши специалисты", "alias": "users:specialists", "icon": "bi-person"},
    # {"title": "Советы психолога", "alias": "psychologist_advice", "icon": "bi-chat-dots"},
    # {"title": "Тестирование", "alias": "testing", "icon": "bi-check-circle"},
    # {"title": "Консультации", "alias": "consultations", "icon": "bi-clipboard"},
    # {"title": "Тренинги", "alias": "trainings", "icon": "bi-briefcase"},
    {"title": "Ваши отзывы", "alias": "information:comments", "icon": "bi-star"},
    {"title": "Ваши предложения", "alias": "information:offers", "icon": "bi-lightbulb"}
]


def custom_404_view(request, exception):
    messages.error(request, "Такой страницы не существует, поэтому Вы перенаправлены на главную страницу сайта")
    return redirect('main')


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'main'
        return context


class OfferView(ListView):
    model = Offer
    template_name = 'offer.html'
    context_object_name = 'offers'
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Offer.objects.prefetch_related('answer').select_related('author').order_by('-published_date')
            else:
                return (Offer.objects.filter(author=self.request.user).
                        prefetch_related('answer').select_related('author').order_by('-published_date'))
        else:
            return Offer.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:offers'
        context['form'] = OfferForm()
        context['answer_form'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.author = request.user
            offer.save()
            messages.success(request, 'Ваше предложение успешно добавлено!')
            page = request.POST.get('page', 1)
            return redirect(f"{reverse('information:offers')}?page={page}")


class CommentView(ListView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comments'
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_staff:
            return (Comment.objects.prefetch_related('answer').
                    select_related('author').order_by('-published_date'))
        else:
            return (Comment.objects.filter(status=2).prefetch_related('answer').
                    select_related('author').order_by('-published_date'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:comments'
        context['form'] = CommentForm()
        context['answer_form'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш отзыв добавлен и находится на модерации!')
            page = request.POST.get('page', 1)
            return redirect(f"{reverse('information:comments')}?page={page}")


class AnswerView(ListView):
    model = Answer
    context_object_name = 'answers'

    def get_queryset(self):
        return Answer.objects.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'information:answers'
        context['form'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answers = form.save(commit=False)
            answers.author = request.user
            offer_id = request.POST.get('offer_id')
            offer = get_object_or_404(Offer, id=offer_id)
            answers.save()
            offer.answer.add(answers)
            messages.success(request, 'Ваш ответ добавлен!')
            page = request.POST.get('page', 1)
            return redirect(f"{reverse('information:offers')}?page={page}")


class AnswerCommentView(ListView):
    model = Answer
    context_object_name = 'answers_comment'

    def get_queryset(self):
        return Answer.objects.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'information:answers_comment'
        context['form'] = AnswerForm()
        return context

    def post(self, request, *args, **kwargs):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answers = form.save(commit=False)
            answers.author = request.user
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            answers.save()
            comment.answer.add(answers)
            messages.success(request, 'Ваш ответ добавлен!')
            page = request.POST.get('page', 1)
            return redirect(f"{reverse('information:comments')}?page={page}")




