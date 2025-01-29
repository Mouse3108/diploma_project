from django.urls import path
from .views import *

app_name = 'events'

urlpatterns = [
    path("consultations/", ConsultationsView.as_view(), name="consultations"),
    path('consultations/<int:pk>/update/', UpdateConsultationClientView.as_view(), name='consultation_update'),
    path('consultations/<int:pk>/cancel/', CancelConsultationClientView.as_view(), name='consultation_cancel'),
    path("trainings/", TrainingsView.as_view(), name="trainings"),
    path("trainings/<int:pk>/update/", UpdateTrainingClientView.as_view(), name="training_update"),
    path('trainings/<int:pk>/cancel/', CancelTrainingClientView.as_view(), name='training_cancel'),
]
