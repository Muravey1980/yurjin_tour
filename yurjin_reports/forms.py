from django import forms
from django.contrib.admin import widgets

class PeriodForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)