'''
Created on 2017-03-30
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
#from django.core.urlresolvers import reverse_lazy
#import datetime
#from _datetime import date
#from django import forms
#from calendar import month
#from yurjin_journal.models import  Office

from django.views.generic.base import TemplateView
from yurjin_journal.models import Manager
from django.db.models import Count,Sum

from . import forms

from django.views.generic.edit import FormView
from datetime import datetime, date, timedelta 


class ReportIndexView(TemplateView):
    template_name = 'yurjin_reports/index.html' 

    def get_context_data(self, **kwargs):
        context=super(ReportIndexView,self).get_context_data(**kwargs)
        context['form'] = forms.PeriodForm()
        return context


class PeriodReportViewAjax(FormView):
    pass

class PeriodReportView(FormView): 
    #model = Office
    template_name = 'yurjin_reports/period_report.html'
    form_class = forms.PeriodForm
    #form= forms.PeriodForm()
    #date_from = None#datetime.date(2017,1,1)
    #date_to   = None#datetime.date(2017,5,31)
    
    #success_url='period_report'
    
    #def post(self, request, *args, **kwargs):
    #    self.date_from = datetime.datetime.strptime(self.request.GET.get('date_from','01.01.2017'),'%d.%m.%Y')
    #    self.date_to   = datetime.datetime.strptime(self.request.GET.get('date_to','31.05.2017'),'%d.%m.%Y')
    #    return super(PeriodReportView, self).post(self, request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        date_to_default = date.today().replace(day=1)-timedelta(days=1)
        date_from_default = date_to_default.replace(day=1)
        self.date_from = datetime.strptime(self.request.GET.get('date_from',format(date_from_default,'%d.%m.%Y'))+' 00:00:00','%d.%m.%Y %H:%M:%S')
        self.date_to   = datetime.strptime(self.request.GET.get('date_to',format(date_to_default,'%d.%m.%Y'))+' 23:59:59','%d.%m.%Y %H:%M:%S')
        return super(PeriodReportView, self).get(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context=super(PeriodReportView,self).get_context_data(**kwargs)
        context['date_from'] = self.date_from
        context['date_to'] = self.date_to
        context['form'] = forms.PeriodForm()
        #context['contract_list'] = Contract.objects.annotate(tourist_count=Count('tourist_list'))
        #context['office_list'] = Office.objects.annotate(total_count=Count('contract'),total_sum=Sum('contract__contract_sum'))
        context['manager_list'] = Manager.objects.filter(contract__contract_date__range=(self.date_from,self.date_to)).annotate(total_count=Count('contract'),total_sum=Sum('contract__contract_sum'),total_margin=Sum('contract__contract_sum')-Sum('contract__operator_sum')).order_by('office')
        return context

