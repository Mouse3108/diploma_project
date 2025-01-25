from django import forms
from .models import *
from django.utils.text import slugify
from unidecode import unidecode


class OfferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Offer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'id': 'id_text', 'required': True}),
        }
        labels = {'text': 'Ваше предложение или пожелание'}

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ['text', 'category']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5, 'id': 'id_text', 'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select', 'required': True
            }),
        }
        labels = {
            'text': 'Ваш отзыв',
            'category': 'Категория отзыва'
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'id': 'id_text', 'required': True}),
        }
        labels = {'text': 'Ответ специалиста'}

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

