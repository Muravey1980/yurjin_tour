'''
Created on 2016-10-31
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
#from __future__ import absolute_import, unicode_literals
#from django.utils.encoding import force_text
#from __future__ import __all__

#import dal
#from django.conf import settings
#from django.templatetags.i18n import language

#from django.utils import timezone
#from django.forms.models import inlineformset_factory
#from django.forms.models import modelformset_factory

from django.core.exceptions import ValidationError

from django import forms
from django.contrib.admin import widgets
from dal import autocomplete
from .models import Contract, Tourist, Manager, Payment, Resort    #, Status #, PaymentMethod


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        #fields = ['contract_num', 'contract_date', 'tourist_list']
        #fields = ('__all__')
        fields = [
            #'manager',
            #'contract_num', 
            'contract_date', 'client',
            'tour_begin_date', 'tour_finish_date',
            'contract_sum', 
            #'prepayment_sum',
            'tourist_list', 'tour_operator', 'resort',
            'hotel_name','room_type','hotel_begin_date', 'hotel_finish_date',
            'board',
            'transfer',
            #'excursion',
            'russian_guide','visa_support',
            'medical_insurance','non_departure_insurance','visa_risk_insurance',
            #'payments',
            'excursions',
            'confirm_date',
            'doc_issue_date',
            'full_pay_date',
            'operator_sum'
            #,'status'
            ]
        
        widgets = {
            #'contract_date': forms.SelectDateWidget(years=range(timezone.now().year-3,timezone.now().year+3)),
            #'contract_num': autocomplete,
            #'contract_date': forms.SelectDateWidget(),
            #'contract_date': widgets.AdminDateWidget(format='%d/%m/%Y'),
            
            'contract_date': widgets.AdminDateWidget(),
                        
            #'manager': autocomplete.ModelSelect2(),
            #'office': autocomplete.ModelSelect2(),
            'client': autocomplete.ModelSelect2(),
            'status': autocomplete.ModelSelect2(),
            
            'tour_begin_date': widgets.AdminDateWidget(),
            'tour_finish_date': widgets.AdminDateWidget(),
            
            
            #'signatory': autocomplete.ModelSelect2(),
            'tourist_list': autocomplete.ModelSelect2Multiple(url='yurjin_journal:tourist_select'),
            #'tourist_list': TouristList(url='tourist_list'),
            'tour_operator': autocomplete.ModelSelect2(),
            'resort': autocomplete.ModelSelect2(),
            'hotel_begin_date': widgets.AdminDateWidget(),
            'hotel_finish_date': widgets.AdminDateWidget(),
            'room_type': autocomplete.ModelSelect2(),
            'board': autocomplete.ModelSelect2(),
            
            'confirm_date': widgets.AdminDateWidget(),
            'doc_issue_date': widgets.AdminDateWidget(),
            'full_pay_date': widgets.AdminDateWidget(),
            #'doc_get_date': widgets.AdminDateWidget(),
        }

    def clean(self):
        cleaned_data = super(ContractForm, self).clean()
        if cleaned_data['contract_sum'] <= 0:
            #raise ValidationError('Сумма контракта не может быть меньше нуля',code = 'invalid')
            raise ValidationError('Не заполнена сумма контракта',code = 'invalid')
        if cleaned_data['tour_begin_date'] == None:
            raise ValidationError('Не указана дата начала тура',code = 'invalid')
        if cleaned_data['tour_finish_date'] == None:
            raise ValidationError('Не указана дата окончания тура',code = 'invalid')
        if cleaned_data['hotel_begin_date'] == None:
            raise ValidationError('Не указана дата заселения в отель',code = 'invalid')
        if cleaned_data['hotel_finish_date'] == None:
            raise ValidationError('Не указана дата выписки из отеля',code = 'invalid')
        if cleaned_data['tour_finish_date'] and cleaned_data['tour_begin_date']:
            if cleaned_data['tour_finish_date'] < cleaned_data['tour_begin_date']:
                raise ValidationError('Дата окончания тура не может быть меньше даты начала тура',code = 'invalid')
        if cleaned_data['hotel_finish_date'] and cleaned_data['hotel_begin_date']:    
            if cleaned_data['hotel_finish_date'] < cleaned_data['hotel_begin_date']:
                raise ValidationError('Дата выезда из отеля не может быть меньше даты въезда в отель',code = 'invalid')
        if cleaned_data['hotel_begin_date'] and cleaned_data['tour_begin_date']:    
            if cleaned_data['hotel_begin_date'] < cleaned_data['tour_begin_date']:
                raise ValidationError('Дата въезда в отель не может быть меньше даты начала тура ',code = 'invalid')
        if cleaned_data['tour_finish_date'] and cleaned_data['hotel_finish_date']:    
            if cleaned_data['tour_finish_date'] < cleaned_data['hotel_finish_date']:
                raise ValidationError('Дата окончания тура не может быть меньше даты выезда из отеля',code = 'invalid')
        
        if cleaned_data['tour_begin_date'] and cleaned_data['confirm_date']:    
            if cleaned_data['tour_begin_date'] < cleaned_data['confirm_date']:
                raise ValidationError('Дата начала тура не может быть меньше даты подтверждения тура',code = 'invalid')
        #if cleaned_data['doc_issue_date'] and cleaned_data['confirm_date']:    
        #    if cleaned_data['doc_issue_date'] < cleaned_data['confirm_date']:
        #        raise ValidationError('Дата выдачи документов не может быть меньше даты подтверждения тура',code = 'invalid')
        #if cleaned_data['tour_begin_date'] and cleaned_data['full_pay_date']:    
        #    if cleaned_data['tour_begin_date'] < cleaned_data['full_pay_date']:
        #        raise ValidationError('Дата начала тура не может быть меньше даты полной оплаты',code = 'invalid')
        
        
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['tourist_list'].count() == 0:
            raise ValidationError('Не заполнено поле "Список туристов"',code = 'invalid')
        if cleaned_data['contract_sum'] == None:
            raise ValidationError('Не заполнено поле "Сумма контракта"',code = 'invalid')
        if cleaned_data['tour_operator'] == None:
            raise ValidationError('Не выбран туроператор',code = 'invalid')
        if cleaned_data['resort'] == None:
            raise ValidationError('Не выбран курорт',code = 'invalid')
        if cleaned_data['hotel_name'].strip() == '':
            raise ValidationError('Не заполнено поле "Отель"',code = 'invalid')
        if cleaned_data['room_type'] == None:
            raise ValidationError('Не выбран тип номера',code = 'invalid')
        if cleaned_data['board'] == None:
            raise ValidationError('Не выбран тип питания',code = 'invalid')

        
        
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        if cleaned_data['client'] == None:
            raise ValidationError('Не заполнено поле "клиент"',code = 'invalid')
        #if cleaned_data['_date'] == None:
        #    raise ValidationError('Не указана дата ',code = 'invalid')
        #if cleaned_data['_date'] == None:
        #    raise ValidationError('Не указана дата ',code = 'invalid')
        #if cleaned_data['_date'] == None:
        #    raise ValidationError('Не указана дата ',code = 'invalid')
        #if cleaned_data['prepayment_sum'] < 0:
        #    raise ValidationError('Сумма предоплаты не может быть меньше нуля',code = 'invalid')    
        #if cleaned_data['contract_sum'] < cleaned_data['prepayment_sum']:    
        #    raise ValidationError('Сумма предоплаты не может быть больше суммы контракта',code = 'invalid')
        
            
        return cleaned_data
         
    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        if hasattr(self.instance, 'status')==False:
            del self.fields['confirm_date']
        if hasattr(self.instance, 'status')==False or self.instance.status.status_name=='signed':
            del self.fields['doc_issue_date']
            del self.fields['full_pay_date']
            del self.fields['operator_sum']  
        

class TouristForm(forms.ModelForm):
    class Meta:
        model = Tourist
        exclude = ['office',]
        widgets = {    
            'birthdate': widgets.AdminDateWidget(),
            'passport_date': widgets.AdminDateWidget(),
            'international_passport_date_of_expiry': widgets.AdminDateWidget(),
            }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
                'contract',
                'payment_method',
                'payment_sum'
                ]
        
        widgets = {
            #'payment_date': widgets.AdminDateWidget(),
            #'payment_method': autocomplete.ModelSelect2(),
            'contract': autocomplete.ModelSelect2(),
            }
    
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        if cleaned_data['payment_sum'] <= 0:
            raise ValidationError('Сумма платежа должна быть положительным числом',code = 'invalid')        


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['last_name', 'first_name', 'mid_name', 'full_name_r']


class ResortForm(forms.ModelForm):
    class Meta:
        model = Resort
        fields = [
                'country',
                'resort_name'
                ]
        
        widgets = {
            'country': autocomplete.ModelSelect2(),
            }

#PaymentFormset = modelformset_factory(Payment, form=PaymentForm,can_delete=True)