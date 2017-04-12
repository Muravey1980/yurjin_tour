'''
Created on 2016-10-26
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''

from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login, logout

from . import views

app_name = 'yurjin_journal'
urlpatterns = [
    #Аутентификация
    url(r'^login/', login, name = 'login'),
    url(r'^logout/', logout, {"next_page": 'yurjin_main:index'}, name = 'logout'),
    url(r'^profile/$', login_required(views.ProfileUpdateView.as_view()), name='profile_edit'),
    
    #Отчеты
    #url(r'^yurjin_reports/$', login_required(views.ReportIndex.as_view()), name='report_index'),
    
    #Договоры
    url(r'^$', login_required(views.ContractListView.as_view()), name='index'),    
    url(r'^contracts/$', login_required(views.ContractArchiveIndexView.as_view()), name='contract_archive'),
    url(r'^contracts/(?P<year>[0-9]{4})/$', login_required(views.ContractYearArchiveView.as_view()), name='contract_archive_year'),
    url(r'^contracts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', login_required(views.ContractMonthArchiveView.as_view()), name='contract_archive_month'),
    
    url(r'^contract/add/$', permission_required('yurjin_journal.add_contract')(views.ContractCreateView.as_view()),name = 'contract_add'),
    url(r'^contract/(?P<pk>[0-9]+)/edit/$', permission_required('yurjin_journal.change_contract')(views.ContractUpdateView.as_view()), name='contract_edit'),
    url(r'^contract/(?P<pk>[0-9]+)/delete/$', permission_required('yurjin_journal.delete_contract')(views.ContractDeleteView.as_view()),name = 'contract_delete'),
    url(r'^contract/(?P<pk>[0-9]+)/preview/$', login_required(views.ContractPreview.as_view()), name='contract_preview'),
    url(r'^contract/(?P<pk>[0-9]+)/print/$', login_required(views.ContractPrintView.as_view()), name='contract_print'),   
    
    
    #Туристы
    url(r'^tourist_list/$',views.TouristList.as_view(),name='tourist_select'),
    url(r'^tourists/$', login_required(views.TouristListView.as_view()), name='tourist_list'),
    url(r'^tourist/add/$', permission_required('yurjin_journal.add_contract')(views.TouristCreateView.as_view()),name = 'tourist_add'),
    url(r'^tourist/(?P<pk>[0-9]+)/edit/$', permission_required('yurjin_journal.change_contract')(views.TouristUpdateView.as_view()), name='tourist_edit'),
    url(r'^tourist/(?P<pk>[0-9]+)/delete/$', permission_required('yurjin_journal.delete_contract')(views.TouristDeleteView.as_view()),name = 'tourist_delete'),
    
    
    #Курорты
    url(r'^resorts/$', login_required(views.ResortListView.as_view()), name='resort_list'),
    url(r'^resort/add/$', permission_required('yurjin_journal.add_resort')(views.ResortCreateView.as_view()),name = 'resort_add'),
    url(r'^resort/(?P<pk>[0-9]+)/edit/$', permission_required('yurjin_journal.change_resort')(views.ResortUpdateView.as_view()), name='resort_edit'),
    url(r'^resort/(?P<pk>[0-9]+)/delete/$', permission_required('yurjin_journal.delete_resort')(views.ResortDeleteView.as_view()),name = 'resort_delete'),
    
    
    #Платежи
    url(r'^payments/$', login_required(views.PaymentListView.as_view()), name='payment_list'),
    #url(r'^payment/add/(?:\?contract_id=(?P<contract_id>\d+))?$', permission_required('yurjin_journal.add_payment')(views.PaymentCreateView.as_view()),name = 'payment_add'),
    url(r'^payment/add/$', permission_required('yurjin_journal.add_payment')(views.PaymentCreateView.as_view()),name = 'payment_add'),
    url(r'^payment/(?P<pk>[0-9]+)/delete/$', permission_required('yurjin_journal.delete_payment')(views.PaymentDeleteView.as_view()),name = 'payment_delete'),
    url(r'^payment/(?P<pk>[0-9]+)/print/$', login_required(views.PaymentPrintView.as_view()), name='payment_print'),
    

]

"""
Закомментировано в связи с тем, что пока не используется
    #url(r'^(?P<page>[0-9])*$', login_required(views.IndexView.as_view()), name='index'),
    #url(r'^(?P<page>[0-9])*$', login_required(views.ContractListView.as_view()), name='index'),
    #url(r'^contracts$', views.ContractListView.as_view(), name='contract_list'),
    #url(r'^contract/(?P<pk>[0-9]+)/print/$', login_required(views.ContractPdfPrint.as_view()), name='contract_pdf_print'),
    #url(r'^contract/(?P<pk>[0-9]+)/edit_test/$', views.ContractEditTest.as_view(), name='edit_test'),
    #url(r'^contract/(?P<contract_id>[0-9]+)/save$', views.contract_save, name='contract_save'),
    #url(r'^payment/(?P<pk>[0-9]+)/edit/$', permission_required('yurjin_journal.change_payment')(views.PaymentUpdateView.as_view()), name='payment_edit'),
    #url(r'^payments_edit/$', login_required(views.PaymentListEditView.as_view()), name='payment_list_edit'),
"""