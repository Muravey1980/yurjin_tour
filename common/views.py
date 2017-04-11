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
            self.filter = self.request.GET['filter']
        except KeyError:
            self.filter = ""
        try:
            self.paginate_by = self.request.GET['paginate_by']
        except KeyError:
            self.paginate_by = 20


        return super(FilteredAndSortedView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(FilteredAndSortedView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        context['paginate_by'] = self.paginate_by
        return context
    
    def get_queryset(self):
        queryset=self.model.objects.all()
        if (self.request.user.is_superuser):
            pass
        elif (self.request.user.manager == self.request.user.manager.office.tour_agency.director):
            queryset=queryset.filter(office__tour_agency=self.request.user.manager.office.tour_agency)
        else:
            queryset=queryset.filter(office=self.request.user.manager.office)
        
        if (self.filter):
            if(self.model==Contract):
                queryset=queryset.filter(Q(client__last_name__icontains=self.filter) | Q(tourist_list__last_name__icontains=self.filter)).distinct().order_by('-contract_date','-contract_num')
            elif(self.model==Tourist):
                queryset=queryset.filter(last_name__icontains=self.filter).distinct().order_by('last_name', 'first_name', 'mid_name')
            else:
                pass

        return queryset
    
    
    