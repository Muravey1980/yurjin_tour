from django import forms
from django.contrib.admin import widgets
#import datetime

class PeriodForm(forms.Form):
    #class Meta:
    #    fields = ['date_from','date_to']
    #    widgets = {'date_from': widgets.AdminDateWidget(),
    #               'date_to': widgets.AdminDateWidget(),
    #               }
    #date_from = forms.DateField(label='Дата с', widget=widgets.AdminDateWidget(),initial=datetime.date.today)
    
    date_from = forms.DateField(label='Дата с', widget=widgets.AdminDateWidget())
    date_to = forms.DateField(label='Дата по',widget=widgets.AdminDateWidget())#forms.DateField