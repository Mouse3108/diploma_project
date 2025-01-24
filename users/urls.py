from django.urls import path
from .views import *

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
]
