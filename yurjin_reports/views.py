'''
Created on 2017-03-30
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
from django.views.generic.base import TemplateView
from yurjin_journal.models import Manager, Office, Contract, Status
from django.db.models import Count,Max,Sum
import datetime 

from . import forms
#from django import forms

class ReportIndexView(TemplateView):
    template_name = 'yurjin_reports/index.html' 

class PeriodReportView(TemplateView): 
    model = Office
    template_name = 'yurjin_reports/period_report.html'
    #queryset=Office.objects.all()
    date_from = datetime.date(2017,1,1)
    date_to   = datetime.date(2017,5,31)
    
    form = forms.PeriodForm()
    
    def get_context_data(self, **kwargs):
        context=super(PeriodReportView,self).get_context_data(**kwargs)
        context['date_from']=self.date_from
        context['date_to']=self.date_to
        #context['contract_list'] = Contract.objects.annotate(tourist_count=Count('tourist_list'))
        #context['office_list'] = Office.objects.annotate(total_count=Count('contract'),total_sum=Sum('contract__contract_sum'))
        #status=Status.objects.get(status_name='closed')
        #,contract__contract_status__status_name='closed'
        context['manager_list'] = Manager.objects.filter(contract__contract_date__range=(self.date_from,self.date_to)).annotate(total_count=Count('contract'),total_sum=Sum('contract__contract_sum')).order_by('office')
        return context