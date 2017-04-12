'''
Created on 2017-03-20
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
from django.views.generic.base import View
from django.db.models import Q


from yurjin_journal.models import Contract,Tourist

class FilteredAndSortedView(View):
    def get(self, request, *args, **kwargs):
        try:
            self.q = self.request.GET['q']
        except KeyError:
            self.q = ""
        try:
            self.paginate_by = int(self.request.GET['paginate_by'])
        except KeyError:
            self.paginate_by = 20
        try:
            self.is_important = int(self.request.GET['is_important'])
        except KeyError:
            self.is_important = None 
        
        return super(FilteredAndSortedView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(FilteredAndSortedView, self).get_context_data(**kwargs)
        context['q'] = self.q
        context['paginate_by'] = self.paginate_by
        context['is_important'] = self.is_important
        return context
    
    def get_queryset(self):
        queryset=self.model.objects.all()
        if (self.request.user.is_superuser):
            pass
        elif (self.request.user.manager == self.request.user.manager.office.tour_agency.director):
            queryset=queryset.filter(office__tour_agency=self.request.user.manager.office.tour_agency)
        else:
            queryset=queryset.filter(office=self.request.user.manager.office)
        
        if (self.q):
            if(self.model==Contract):
                queryset=queryset.filter(Q(client__last_name__icontains=self.q) | Q(tourist_list__last_name__icontains=self.q)).distinct()
            elif(self.model==Tourist):
                queryset=queryset.filter(last_name__icontains=self.q).distinct()
            else:
                pass
        
        #Только важные
        if(self.model==Contract):
            if (self.is_important==1):
                queryset=queryset.filter(
                    Q(confirm_date=None) | #Нет даты подтверждения
                    (~Q(confirm_date=None) & Q(doc_issue_date=None)) #Есть дата подтверждения и нет даты выдачи документов
                    #(~Q(confirm_date=None) & () ) Добавить если есть дата подтвеждения и нет полной оплаты
                    )
        
            
                
        #
            
            #
        #queryset=queryset.filter(confirm_date=None).distinct()
        
        #Сортировка
        if(self.model==Contract):
            queryset=queryset.order_by('-contract_date','-contract_num')
        elif(self.model==Tourist):
            queryset=queryset.order_by('last_name', 'first_name', 'mid_name')
        else:
            pass
        
        return queryset
    
    
    