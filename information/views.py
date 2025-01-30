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
    template_name = 'offer/offer.html'
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
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
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
    template_name = 'comment/comment.html'
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
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
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


class ClientCommentView(ListView):
    model = Comment
    template_name = 'client/client_comment.html'
    context_object_name = 'client_comments'

    def get_queryset(self):
        return (Comment.objects.filter(author=self.request.user).prefetch_related('answer').
                select_related('author').order_by('-published_date'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:client_comments'
        return context


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
        context['page_alias'] = 'information:comment'
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


class ArticlesView(ListView):
    model = Article
    template_name = 'article/articles.html'
    context_object_name = 'articles'
    paginate_by = 4

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = (Article.objects.prefetch_related('positive_grade', 'negative_grade').
                        select_related('category').
                        order_by("-published_date"))
        else:
            queryset = (Article.objects.filter(status=1).
                        prefetch_related('positive_grade', 'negative_grade').
                        select_related('category').
                        order_by("-published_date"))
        search_query = unquote(self.request.GET.get("search", ""))
        if search_query:
            query = Q(title__icontains=search_query) | Q(text__icontains=search_query)
            queryset = queryset.filter(query)
        queryset = queryset.distinct().order_by("-published_date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:articles'
        search_query = unquote(self.request.GET.get("search", ""))
        context['search_query'] = urlencode({'search': search_query})
        context['categories'] = Category.objects.order_by("name")
        return context


class ArticlesByCategoryView(ListView):
    model = Article
    template_name = 'article/articles.html'
    context_object_name = 'articles'
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        if self.request.user.is_staff:
            queryset = (Article.objects.filter(category__slug=self.kwargs['slug']).
                        prefetch_related('positive_grade', 'negative_grade').
                        select_related('category').
                        order_by("-published_date"))
        else:
            queryset = (Article.objects.filter(status=1, category__slug=self.kwargs['slug']).
                        prefetch_related('positive_grade', 'negative_grade').
                        select_related('category').
                        order_by("-published_date"))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:articles'
        context['categories'] = Category.objects.order_by("name")
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return (Article.objects.prefetch_related('positive_grade', 'negative_grade').
                select_related('category'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:articles'
        context['categories'] = Category.objects.order_by("name")
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if f'article_{self.object.id}_viewed' not in request.session and not request.user.is_staff:
            Article.objects.filter(slug=self.object.slug).update(views=F('views') + 1)
            request.session[f'article_{self.object.id}_viewed'] = True
            self.object.refresh_from_db()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class NegativeGradeArticleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        user = request.user
        positive_grade = article.positive_grade.filter(id=user.id).exists()
        negative_grade = article.negative_grade.filter(id=user.id).exists()
        if not negative_grade:
            if not positive_grade:
                article.negative_grade.add(user)
        else:
            article.negative_grade.remove(user)
        return JsonResponse({
            'positive_grade': positive_grade,
            'negative_grade': negative_grade,
            'positive_grade_count': article.positive_grade.count(),
            'negative_grade_count': article.negative_grade.count()
        })


class PositiveGradeArticleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)
        user = request.user
        positive_grade = article.positive_grade.filter(id=user.id).exists()
        negative_grade = article.negative_grade.filter(id=user.id).exists()
        if not positive_grade:
            if not negative_grade:
                article.positive_grade.add(user)
        else:
            article.positive_grade.remove(user)
        return JsonResponse({
            'positive_grade': positive_grade,
            'negative_grade': negative_grade,
            'positive_grade_count': article.positive_grade.count(),
            'negative_grade_count': article.negative_grade.count()
        })


class CommentsByCategoryView(ListView):
    model = Comment
    template_name = 'comment/comment.html'
    context_object_name = 'comments'
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_staff:
            return (Comment.objects.prefetch_related('answer').
                    filter(category=self.kwargs.get('category')).
                    select_related('author').order_by('-published_date'))
        else:
            return (Comment.objects.filter(status=2, category=self.kwargs.get('category')).
                    prefetch_related('answer').
                    select_related('author').order_by('-published_date'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'information:comments'
        context['form'] = CommentForm()
        context['answer_form'] = AnswerForm()
        context['is_blacklisted'] = self.request.user.groups.filter(name='Черный список').exists()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            messages.success(request, 'Ваш отзыв добавлен и находится на модерации!')
            page = request.POST.get('page', 1)
            return redirect(f"{reverse('information:comments_category')}?page={page}")
