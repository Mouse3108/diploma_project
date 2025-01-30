from django.contrib import admin
from users.models import *
from events.models import *
from information.models import *
from tests.models import *


@admin.register(TestResults)
class TestResultsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'testing_date', 'client', 'balls', 'result'
    )
    list_display_links = (
        'name', 'testing_date', 'balls', 'result'
    )
    search_fields = (
        'name', 'testing_date', 'client', 'result'
    )
    list_filter = (
        'name', 'testing_date', 'client'
    )
    readonly_fields = (
        'name', 'testing_date', 'client', 'balls', 'result'
    )


@admin.register(FunnyTest)
class FunnyTestAdmin(admin.ModelAdmin):
    list_display = (
        'question', 'answer1', 'answer2', 'correct_answer'
    )
    list_display_links = (
        'question', 'answer1', 'answer2', 'correct_answer'
    )


@admin.register(FunnyTestResult)
class FunnyTestResult(admin.ModelAdmin):
    list_display = (
        'min_balls', 'max_balls', 'result'
    )
    list_display_links = (
        'min_balls', 'max_balls', 'result'
    )
    search_fields = (
        'min_balls', 'max_balls'
    )
    list_filter = (
        'min_balls', 'max_balls'
    )


@admin.register(WordExclusionTest)
class WordExclusionTest(admin.ModelAdmin):
    list_display = (
        'question', 'answer1', 'answer2', 'answer3',
        'answer4', 'answer5', 'correct_answer'
    )
    list_display_links = (
        'question', 'answer1', 'answer2', 'answer3',
        'answer4', 'answer5', 'correct_answer'
    )


@admin.register(WordExclusionTestResult)
class WordExclusionTestResult(admin.ModelAdmin):
    list_display = (
        'min_balls', 'max_balls', 'result'
    )
    list_display_links = (
        'min_balls', 'max_balls', 'result'
    )
    search_fields = (
        'min_balls', 'max_balls'
    )
    list_filter = (
        'min_balls', 'max_balls'
    )

