from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from users.models import MyUser


class ConsultationUpdateForm(forms.ModelForm):
    client_firstname = forms.CharField(label='Ваше имя', required=True,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'max_length': 150}))
    client_lastname = forms.CharField(label='Ваша фамилия', required=True,
                                      widget=forms.TextInput(
                                          attrs={'class': 'form-control', 'max_length': 150}))
    client_date_birth = forms.DateField(label='Дата рождения', required=True,
                                        widget=forms.DateInput(
                                            attrs={'class': 'form-control', 'type': 'date'}))
    client_phone = forms.CharField(label='Телефон', required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'max_length': 20}))
    client_email = forms.EmailField(label='Электронная почта', required=True,
                                    widget=forms.EmailInput(
                                        attrs={'class': 'form-control', 'max_length': 254}))

    class Meta:
        model = Consultation
        fields = ['client_firstname', 'client_lastname', 'client_date_birth',
                  'client_email', 'client_phone', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'description': 'Обязательно заполните это поле!'
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        self.fields['client_firstname'].initial = self.current_user.first_name or ''
        self.fields['client_lastname'].initial = self.current_user.last_name or ''
        self.fields['client_date_birth'].initial = self.current_user.date_birth or ''
        self.fields['client_phone'].initial = self.current_user.phone or ''
        self.fields['client_email'].initial = self.current_user.email or ''

    def clean(self):
        cleaned_data = super().clean()
        consultation = self.instance
        if consultation.status != 0:
            raise forms.ValidationError("К сожалению, это время уже занято. Выберите другое")
        if not all([cleaned_data.get('client_firstname'),
                    cleaned_data.get('client_lastname'),
                    cleaned_data.get('client_phone'),
                    cleaned_data.get('client_email'),
                    cleaned_data.get('client_date_birth'),
                    cleaned_data.get('description')
                    and cleaned_data['description'].strip() != 'Причина обращения к психологу'
                    ]):
            raise forms.ValidationError("Все поля обязательно должны быть заполнены.")
        return cleaned_data

    def save(self, commit=True):
        consultation = super().save(commit=False)
        consultation.status = 2
        client = self.current_user
        client.first_name = self.cleaned_data['client_firstname']
        client.last_name = self.cleaned_data['client_lastname']
        client.phone = self.cleaned_data['client_phone']
        client.email = self.cleaned_data['client_email']
        client.date_birth = self.cleaned_data['client_date_birth']
        if commit:
            client.save()

        if commit:
            consultation.client = client
            consultation.save()
        return consultation


class TrainingUpdateForm(forms.ModelForm):
    client_firstname = forms.CharField(label='Ваше имя', required=True,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'max_length': 150}))
    client_lastname = forms.CharField(label='Ваша фамилия', required=True,
                                      widget=forms.TextInput(
                                          attrs={'class': 'form-control', 'max_length': 150}))
    client_date_birth = forms.DateField(label='Дата рождения', required=True,
                                        widget=forms.DateInput(
                                            attrs={'class': 'form-control', 'type': 'date'}))
    client_phone = forms.CharField(label='Телефон', required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'max_length': 20}))
    client_email = forms.EmailField(label='Электронная почта', required=True,
                                    widget=forms.EmailInput(
                                        attrs={'class': 'form-control', 'max_length': 254}))
    client_child = forms.CharField(label='Имя и возраст Вашего ребенка', required=True,
                                   widget=forms.Textarea(
                                       attrs={'class': 'form-control', 'rows': 1}))

    class Meta:
        model = Training
        fields = ['client_firstname', 'client_lastname', 'client_date_birth',
                  'client_email', 'client_phone', 'client_child']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        self.training = kwargs.pop('training', None)
        super().__init__(*args, **kwargs)
        self.fields['client_firstname'].initial = self.current_user.first_name or ''
        self.fields['client_lastname'].initial = self.current_user.last_name or ''
        self.fields['client_date_birth'].initial = self.current_user.date_birth or ''
        self.fields['client_phone'].initial = self.current_user.phone or ''
        self.fields['client_email'].initial = self.current_user.email or ''
        if self.training.psychologists.filter(job_title='Детский психолог').exists():
            self.fields['client_child'].initial = self.current_user.job_speciality or ''
            self.fields['client_child'].widget.attrs['style'] = 'display: block;'
        else:
            self.fields['client_child'].initial = self.current_user.job_speciality or 'Информация отсутствует'
            self.fields['client_child'].widget.attrs['style'] = 'display: none;'
            self.fields['client_child'].label = ''

    def clean(self):
        cleaned_data = super().clean()
        training = self.instance
        if training.clients.count() == training.count_clients:
            raise forms.ValidationError("К сожалению, на этом тренинге мест больше нет. "
                                        "Пожалуйста, выберите другое мероприятие")
        if not all([cleaned_data.get('client_firstname'),
                    cleaned_data.get('client_lastname'),
                    cleaned_data.get('client_phone'),
                    cleaned_data.get('client_email'),
                    cleaned_data.get('client_date_birth'),
                    cleaned_data.get('client_child')
                    ]):
            raise forms.ValidationError("Все поля обязательно должны быть заполнены.")
        return cleaned_data

    def save(self, commit=True):
        training = super().save(commit=False)
        client = self.current_user
        client.first_name = self.cleaned_data['client_firstname']
        client.last_name = self.cleaned_data['client_lastname']
        client.phone = self.cleaned_data['client_phone']
        client.email = self.cleaned_data['client_email']
        client.date_birth = self.cleaned_data['client_date_birth']
        client.job_speciality = self.cleaned_data['client_child']
        if commit:
            client.save()

        if commit:
            training.clients.add(client)
            training.save()
        return training
