'''
Created on 2017-03-30
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
from django.conf.urls import url
from yurjin_reports.views import ReportIndexView, PeriodReportView 

app_name = 'yurjin_reports'
urlpatterns = [
  #url(r'^$', index, name = "index"),
  url(r'^$', ReportIndexView.as_view(), name = "index"),
  url(r'^period_report$', PeriodReportView.as_view(), name = "period_report"),
]