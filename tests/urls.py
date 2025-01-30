from django.urls import path, reverse_lazy
from users.views import *
from information.views import *
from events.views import *
from tests.views import *
from django.contrib.auth import views as auth_views

app_name = 'tests'

urlpatterns = [
    path('all-tests/', AllTests.as_view(), name='testing'),
    path('funny-test/', FunnyTestView.as_view(), name='funny_test'),
    path('funny-test/result/', FunnyTestResultView.as_view(), name='funny_test_result'),
    path('test-word-exclusion/', WordExclusionTestView.as_view(), name='test_word_exclusion'),
    path('test-word-exclusion/result/', WordExclusionTestResultView.as_view(), name='test_word_exclusion_result'),
]

