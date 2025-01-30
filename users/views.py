from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from users.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, CreateView, UpdateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from .forms import *
from information.urls import *
from django.utils.http import urlencode
from urllib.parse import unquote
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.views import View

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


class RegisterView(View):
    template_name = 'all_users/register.html'

    def get(self, request):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form, 'menu': menu})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Регистрация прошла успешно! Вы можете войти.')
            return redirect('users:login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки!')
        return render(request, self.template_name, {'form': form, 'menu': menu})


class LoginView(View):
    template_name = 'all_users/login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form, 'menu': menu})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                return redirect('main')
            else:
                messages.error(request, 'Неверные учетные данные. Попробуйте снова.')
        return render(request, self.template_name, {'form': form, 'menu': menu})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Вы вышли из системы.')
        return redirect('main')


class SpecialistsView(ListView):
    model = MyUser
    template_name = 'personal/specialists.html'
    context_object_name = 'specialists'

    def get_queryset(self):
        return MyUser.objects.filter(is_staff=True, is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:specialists'
        return context


class SpecialistDetailView(DetailView):
    model = MyUser
    template_name = 'personal/specialist_detail.html'
    context_object_name = 'specialist'

    def get_queryset(self):
        return MyUser.objects.prefetch_related('psychologist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['page_alias'] = 'users:specialists'
        context['education'] = self.object.psychologist.all()
        return context


class ClientDetailView(DetailView):
    model = MyUser
    template_name = 'client/client.html'
    context_object_name = 'client'

    def get_queryset(self):
        return MyUser.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            messages.error(request, 'Не надо подсматривать личные данные другого человека!!!')
            return redirect(reverse('users:client', kwargs={'pk': request.user.pk}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = ClientUpdateForm
    template_name = 'client/client_update.html'

    def get_success_url(self):
        return reverse_lazy('users:client', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            return redirect(reverse('users:client_update', kwargs={'pk': request.user.pk}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def form_valid(self, form):
        new_avatar = form.cleaned_data.get('avatar')
        if new_avatar:
            form.instance.avatar = new_avatar
        else:
            form.instance.avatar = self.get_object().avatar
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'client/change_password.html'

    def get_success_url(self):
        return reverse_lazy('users:client_update', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class PersonalDetailView(DetailView):
    model = MyUser
    template_name = 'personal/personal.html'
    context_object_name = 'personal'

    def get_queryset(self):
        return MyUser.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            return redirect(reverse('users:personal', kwargs={'pk': request.user.pk}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


class PersonalUpdateView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = PersonalUpdateForm
    template_name = 'personal/personal_update.html'

    def get_success_url(self):
        return reverse_lazy('users:personal', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            return redirect(reverse('users:personal_update', kwargs={'pk': request.user.pk}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ChangePasswordPersonalView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'personal/change_password_personal.html'

    def get_success_url(self):
        return reverse_lazy('users:personal_update', kwargs={'pk': self.request.user.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context


