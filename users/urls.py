from django.urls import path, reverse_lazy
from users.views import *
from information.views import *
from events.views import *
from tests.views import *
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('specialists/', SpecialistsView.as_view(), name='specialists'),
    path('specialists/<int:pk>/', SpecialistDetailView.as_view(), name='specialist_detail'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client_update'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('personal/<int:pk>/', PersonalDetailView.as_view(), name='personal'),
    path('personal/<int:pk>/update/', PersonalUpdateView.as_view(), name='personal_update'),
    path('change-password-personal/', ChangePasswordPersonalView.as_view(), name='change_password_personal'),
    path('client/<int:pk>/comments/', ClientCommentView.as_view(), name='client_comments'),
    path('client/<int:pk>/consultations/', ClientConsultationView.as_view(), name='client_consultations'),
    path('client/<int:pk>/trainings/', ClientTrainingView.as_view(), name='client_trainings'),
    path('client/<int:pk>/testing/', ClientTestsView.as_view(), name='client_testing'),

    path("password-reset/", auth_views.PasswordResetView.as_view(
            template_name="all_users/password_reset_form.html",
            email_template_name="all_users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ), name="password_reset",
    ),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
            template_name="all_users/password_reset_done.html"
        ), name="password_reset_done",
    ),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="all_users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ), name="password_reset_confirm",
    ),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
            template_name="all_users/password_reset_complete.html",
        ), name="password_reset_complete",
    ),
]
