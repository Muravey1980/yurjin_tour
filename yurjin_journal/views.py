#from django.http import HttpResponse
#from django.shortcuts import get_object_or_404, render
#from django.core.urlresolvers import reverse
#from django.template.context_processors import request
#from lib2to3.fixes.fix_input import context
#from django.views.generic.base import TemplateView
#from django.forms import modelformset_factory
#from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect


from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin


from dal import autocomplete

from .models import Contract, Tourist, Manager, Payment, PaymentMethod, Resort
from common.views import FilteredAndSortedView
from . import forms

class ResortListView(generic.ListView):
    model = Resort


class ResortCreateView(SuccessMessageMixin,generic.CreateView):    
    template_name = 'yurjin_journal/edit_form.html'
    model = Resort
    form_class=forms.ResortForm
    success_url = reverse_lazy('yurjin_journal:resort_list')
    success_message = "Курорт успешно добавлен"       


class ResortUpdateView(SuccessMessageMixin,generic.UpdateView):
    template_name = 'yurjin_journal/edit_form.html'
    model = Resort
    form_class=forms.ResortForm
    success_url = reverse_lazy('yurjin_journal:resort_list')
    success_message = "Курорт успешно изменен"        


class ResortDeleteView(generic.DeleteView):
    model = Resort
    template_name = "yurjin_journal/delete_form.html"
    success_url = reverse_lazy('yurjin_journal:resort_list')
    success_message = "Курорт успешно удален"   
    




class PaymentListView(generic.ListView):
    template_name = 'yurjin_journal/payment_list.html'
    model = Payment
    paginate_by = 50

    def get_queryset(self):
        q=Payment.objects.all()
        #if (self.request.user.is_superuser):
        #    pass
        #elif (self.request.user.manager == self.request.user.manager.office.tour_agency.director):
        #    q=q.filter(contract__in=Contract.objects.filter(office__in=Office.objects.filter(tour_agency=self.request.user.manager.office.tour_agency)))
        #else:
        #    q=q.filter(office=self.request.user.manager.office)
        #if (self.filter):
        #    q=q.filter(tourist_list__in=Tourist.objects.filter(last_name__icontains=self.filter)).distinct()

        #q=q.filter(office=self.request.user.manager.manager_office)
        
        #contract_date__lte=timezone.now()
        #filter=()
        #return Contract.objects.filter(manager=self.request.user.manager,contract_date__lte=timezone.now()).order_by('-contract_date','-contract_num')
        #return Contract.objects.filter(manager=self.request.user.manager,contract_date__lte=timezone.now()).order_by('-contract_date','-contract_num')
        return q.order_by('-payment_date')

    
class PaymentCreateView(generic.CreateView):
    template_name = 'yurjin_journal/edit_form.html'
    model = Payment    
    form_class=forms.PaymentForm
    success_url = reverse_lazy('yurjin_journal:payment_list')
    success_message = "Платеж успешно внесен"
    initial = {
                #'payment_date': timezone.datetime.today(),
                #'payment_method': get_cash_method() 
                #'contract': Contract.objects.get(id=self.request.GET['contract_id'])
                }
    
    #def get_cash_method(self):    
    #    return PaymentMethod.objects.get(method_name='cash_payment'),
    
    def form_valid(self, form):
        form.instance.manager = self.request.user.manager
        form.instance.office = self.request.user.manager.office
        
        return super(PaymentCreateView, self).form_valid(form)    
    
    def get(self, request, *args, **kwargs):
        queryset=PaymentMethod.objects.filter(method_name='cash_payment')
        self.initial['payment_method'] = queryset[0] if len(queryset)==1 else None  
        #if len(queryset)==1:
        #    self.initial['payment_method'] = PaymentMethod.objects.get(method_name='cash_payment')
        #self.initial['payment_method'] = PaymentMethod.objects.get (method_name='cash_payment')
        try:
            contract = Contract.objects.get(id=self.request.GET['contract_id'])
            self.initial["contract"] = contract
            self.initial["payment_sum"] = contract.get_remain_payment_sum()    
        except KeyError:
            self.initial["contract"] = None
                        
        return super(PaymentCreateView, self).get(request, *args, **kwargs)
    

class PaymentDeleteView(generic.DeleteView):
    model = Payment
    template_name = "yurjin_journal/delete_form.html"
    success_url = reverse_lazy('yurjin_journal:payment_list')

    
class PaymentPrintView(generic.DetailView): 
    model = Payment
    template_name = "yurjin_journal/payment_print.html"

    



class ContractListView(FilteredAndSortedView, generic.ListView):
    template_name = 'yurjin_journal/index.html'
    model = Contract
    #paginate_by = 20


class ContractCreateView(SuccessMessageMixin,generic.CreateView):
    def get_num(self):
        last_month_contract = Contract.objects.filter(contract_date__month=timezone.datetime.today().month,contract_date__year=timezone.datetime.today().year).order_by('contract_date','contract_num').last()
        new_num = last_month_contract.contract_num+1 if last_month_contract else 1 

        return new_num

    def form_valid(self, form):
        form.instance.manager = self.request.user.manager
        form.instance.office = self.request.user.manager.office
        form.instance.signatory = self.request.user.manager.office.tour_agency.director
        form.instance.contract_num = self.get_num()
        #form.instance.status = Status.objects.get(name='signed')
        
        return super(ContractCreateView, self).form_valid(form)    
  
    template_name = 'yurjin_journal/edit_form.html'
    model = Contract    
    initial = {
                'contract_date': timezone.datetime.today(),
                }
    #def get_num():
    #    last_contract = Contract.objects.latest(field_name='contract_date')
    #    return last_contract.contract_num+1 if last_contract.contract_date.year==timezone.datetime.today().year else 1 
    
    
    #'contract_date':timezone.datetime.today()}
    #Contract.objects.latest(field_name='contract_date').contract_num+1, 'contract_date':timezone.datetime.now()}
    #from django.db.models import Max
    #Contract.objects.filter(contract_num__year=timezone.datetime.year(timezone.datetime.now())).order_by('-number')[0]+1
    #initial = {'contract_num':Contract.objects.filter().max() (field_name='contract_date').contract_num+1}
    form_class=forms.ContractForm
    success_url = reverse_lazy('yurjin_journal:index')
    success_message = "Договор успешно создан"        


class ContractUpdateView(SuccessMessageMixin,generic.UpdateView):
    template_name = 'yurjin_journal/edit_form.html'
    model = Contract
    form_class=forms.ContractForm
    success_url = reverse_lazy('yurjin_journal:index')
    success_message = "Договор успешно изменен"        

    def form_valid(self, form):
        #form.instance.status = form.instance.get_status()
        
        return super(ContractUpdateView, self).form_valid(form)


class ContractDeleteView(generic.DeleteView):
    model = Contract
    template_name = "yurjin_journal/delete_form.html"
    success_url = reverse_lazy('yurjin_journal:index')
    #success_message = "Договор успешно удален"


class ContractPreview(generic.DetailView):
    model = Contract
    template_name = 'yurjin_journal/contract_preview.html'


class ContractPrintView(generic.DetailView):
    model = Contract
    template_name = 'yurjin_journal/contract_print.html'

    def get(self, request, *args, **kwargs):
        self.print_form=self.request.GET['print_form']
        
        return super(ContractPrintView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context=super(ContractPrintView,self).get_context_data(**kwargs)
        context['print_form']=self.print_form
        
        return context
    
    
    
    

class TouristList(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Tourist.objects.all()
        qs=qs.filter(office__tour_agency=self.request.user.manager.office.tour_agency)
        if self.q:
            qs = qs.filter(last_name__istartswith=self.q)
            
        return qs


class TouristListView(FilteredAndSortedView, generic.ListView):
    model = Tourist


class TouristCreateView(SuccessMessageMixin,generic.CreateView):    
    template_name = 'yurjin_journal/edit_form.html'
    model = Tourist
    form_class=forms.TouristForm
    success_url = reverse_lazy('yurjin_journal:tourist_list')
    success_message = "Даннные туриста успешно добавлены"
    
    def form_valid(self, form):
        form.instance.office = self.request.user.manager.office
        
        return super(TouristCreateView, self).form_valid(form)         


class TouristUpdateView(SuccessMessageMixin,generic.UpdateView):
    template_name = 'yurjin_journal/edit_form.html'
    model = Tourist
    form_class=forms.TouristForm
    #success_url = reverse_lazy('yurjin_journal:tourist_list')
    success_url = reverse_lazy('yurjin_journal:tourist_list')
    success_message = "Данные туриста успешно изменены"
    
    #def get_success_url(self):
    #    success_url = self.kwargs['success_url']
    #    return reverse_lazy(success_url)        


class TouristDeleteView(generic.DeleteView):
    model = Tourist
    template_name = "yurjin_journal/delete_form.html"
    #success_url = reverse_lazy('yurjin_journal:tourist_list')
    success_message = "Данные туриста успешно удалены"    
    


      

class ProfileUpdateView(SuccessMessageMixin,generic.UpdateView):
    def get_object(self):
        return self.request.user.manager
        
    template_name = 'yurjin_journal/edit_form.html'
    model = Manager
    form_class=forms.ProfileForm
    success_url = reverse_lazy('yurjin_journal:index')
    success_message = "Профиль успешно изменен"

