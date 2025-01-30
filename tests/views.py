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
# from .forms import *
import json
from django.utils.http import urlencode
from urllib.parse import unquote
from django.utils.decorators import method_decorator


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


class AllTests(TemplateView):
    template_name = 'tests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'tests:testing'
        return context


class FunnyTestView(ListView):
    model = FunnyTest
    template_name = 'funny_test.html'
    context_object_name = 'questions_test'

    def get_queryset(self):
        return FunnyTest.objects.all().order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'tests:testing'
        return context


class FunnyTestResultView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        correct_answer = int(data.get('score'))
        result = list(FunnyTestResult.objects.
                      filter(min_balls__lte=correct_answer, max_balls__gte=correct_answer).
                      values('result'))[0]['result']
        if request.user.is_authenticated:
            TestResults.objects.create(
                name='Тест на сообразительность',
                client=request.user,
                balls=correct_answer,
                result=result
            )
        return JsonResponse({
            'success': True,
            'result': result,
            'bal': correct_answer
        })


class WordExclusionTestView(ListView):
    model = WordExclusionTest
    template_name = 'word_exclusion.html'
    context_object_name = 'questions_test'

    def get_queryset(self):
        return WordExclusionTest.objects.all().order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'tests:testing'
        return context


class WordExclusionTestResultView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        correct_answer = int(data.get('score'))
        result = list(WordExclusionTestResult.objects.
                      filter(min_balls__lte=correct_answer, max_balls__gte=correct_answer).
                      values('result'))[0]['result']
        if request.user.is_authenticated:
            TestResults.objects.create(
                name='Тест "Исключение слова"',
                client=request.user,
                balls=correct_answer,
                result=result
            )
        return JsonResponse({
            'success': True,
            'result': result,
            'bal': correct_answer
        })


class ClientTestsView(ListView):
    model = TestResults
    template_name = 'client/testing_client.html'
    context_object_name = 'client_tests'

    def get_queryset(self):
        return (TestResults.objects.filter(client=self.request.user).
                order_by('-testing_date'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:client_testing'
        return context
