from django.urls import path
from .views import *

app_name = 'information'

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offers"),
    path('answers/', AnswerView.as_view(), name='answers'),
    path('answers_comment/', AnswerCommentView.as_view(), name='answers_comment'),
    path('comments/', CommentView.as_view(), name='comments'),
]
