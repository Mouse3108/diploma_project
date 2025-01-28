from django.urls import path
from .views import *

app_name = 'information'

urlpatterns = [
    path("offers/", OfferView.as_view(), name="offers"),
    path('answers/', AnswerView.as_view(), name='answers'),
    path('answers_comment/', AnswerCommentView.as_view(), name='answers_comment'),
    path('comments/', CommentView.as_view(), name='comments'),
    path('comments/category/<int:category>/', CommentsByCategoryView.as_view(), name='comments_category'),
    path('articles/', ArticlesView.as_view(), name="articles"),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/category/<slug:slug>/', ArticlesByCategoryView.as_view(), name='article_category'),
    path('articles/<slug:slug>/positive_grade/', PositiveGradeArticleView.as_view(), name='positive_grade_article'),
    path('articles/<slug:slug>/negative_grade/', NegativeGradeArticleView.as_view(), name='negative_grade_article'),
]
