
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
from math import modf

from number_to_text import num2text
from _datetime import timezone
from reportlab.platypus.paragraph import strip
from symbol import except_clause


class Entity(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=200, verbose_name="Название")
    full_name = models.CharField(blank=True, max_length=200, verbose_name="Полное наименование")
    short_name = models.CharField(blank=True, max_length=200, verbose_name="Краткое наименование")
    fact_address = models.CharField(blank=True, max_length=200, verbose_name="Место нахождения")
    post_address = models.CharField(blank=True, max_length=200, verbose_name="Почтовый адрес")    
    inn = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=0, verbose_name="ИНН")
    kpp = models.DecimalField(null=True, blank=True, max_digits=9, decimal_places=0, verbose_name="КПП")
    ogrn = models.DecimalField(null=True, blank=True, max_digits=13, decimal_places=0, verbose_name="ОГРН")
    account = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=0, verbose_name="Расчетный счет")
    corr_account = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=0, verbose_name="Корр. счет")
    phone =  models.CharField(blank=True, max_length=200, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="e-mail")
    
    
    def __str__(self):
        return self.name


class TourOperator(Entity):
    class Meta:
        verbose_name = "Туроператор"
        verbose_name_plural = "Туроператоры"
        ordering = ('name',)
        
    registry_num = models.CharField(max_length=50, verbose_name="Реестровый номер")
    www_address = models.CharField(max_length=50, verbose_name='Адрес сайта в сети "Интернет"')
    tourpom_member = models.BooleanField(verbose_name='Является членом ассоциации  "ТУРПОМОЩЬ"')

    
class TourAgency(Entity):
    class Meta:
        verbose_name = "Турагентство"
        verbose_name_plural = "Турагентства"
        ordering = ('name',)
    
    director = models.ForeignKey("Manager", on_delete = models.PROTECT, null=True, verbose_name='Директор')


class Country(models.Model):
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ('country_name',)
        
    country_name = models.CharField(max_length=200, unique = True, verbose_name="Название")
    
    def __str__(self):
        return self.country_name


class Resort(models.Model):
    class Meta:
        verbose_name = "Курорт"
        verbose_name_plural = "Курорты"
        unique_together = ('country','resort_name')
        ordering = ('country','resort_name',)
        
    country = models.ForeignKey(Country, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Страна")
    resort_name = models.CharField(max_length=200, verbose_name="Название")

    def __str__(self):
        return self.resort_name
    

class RoomType(models.Model):
    class Meta:
        verbose_name = "Тип номера"
        verbose_name_plural = "Типы номеров"
    
    room_type_name = models.CharField(max_length=50, unique = True, verbose_name='Название')
    room_type_description = models.CharField(blank=True,max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.room_type_name

    
class Board(models.Model):
    class Meta:
        verbose_name = "Тип питания"
        verbose_name_plural = "Типы питания"
    
    board_code = models.CharField(max_length=3, unique = True, verbose_name='Код')
    board_name = models.CharField(max_length=25, verbose_name='Название')
    board_description = models.CharField(blank=True,max_length=200, verbose_name='Описание')

    def __str__(self):
        return self.board_code
    

class Office(models.Model):
    class Meta:
        verbose_name = "Офис"
        verbose_name_plural = "Офисы"
        unique_together = ('tour_agency', 'office_name', 'office_city')
        ordering = ('tour_agency','office_name',)
    
    tour_agency = models.ForeignKey(TourAgency, on_delete = models.PROTECT)
    office_name = models.CharField(max_length=200, verbose_name="Наименование")
    office_adddress = models.CharField(blank=True, max_length=200, verbose_name="Адрес")
    office_city = models.CharField(blank=True, max_length=50, verbose_name="Город")

    def __str__(self):
        return self.office_name
    
    
class Status(models.Model):
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        
    status_name = models.CharField(max_length=50, unique = True, verbose_name="Название")
    status_full_name = models.CharField(max_length=200, verbose_name="Полное наименование")
    
    def __str__(self):
        return self.status_full_name

  
class Person(models.Model):
    class Meta:
        abstract = True
        
    last_name = models.CharField(blank=True, max_length=200, verbose_name="Фамилия")
    first_name = models.CharField(blank=True, max_length=200, verbose_name="Имя")
    mid_name = models.CharField(blank=True, max_length=200, verbose_name="Отчество")
    full_name_r = models.CharField(blank=True, max_length=200, verbose_name="ФИО в родительном падеже")
    office = models.ForeignKey(Office, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Офис")

    def get_fio(self):
        fio = 'ФИО не заполнены'
        if ((self.last_name + self.first_name + self.mid_name).strip() == ''):
            if hasattr(self, 'user'):
                fio = self.user.username
        else:
            fio = self.last_name + ' ' + ((self.first_name[0]+'.') if len(self.first_name)>0 else'')+((self.mid_name[0]+'.') if len(self.mid_name)>0 else '')
        
        return fio 
    
    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.mid_name
    
    def __str__(self):
        return self.get_fio()
 

class Manager(Person):
    class Meta:
        verbose_name = "Менеджер"
        verbose_name_plural = "Менеджеры"
        ordering = ('last_name','first_name', 'mid_name',)
        
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Manager.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.manager.save()


class Tourist(Person):
    class Meta:
        verbose_name = "Турист"
        verbose_name_plural = "Туристы"
        unique_together = ('last_name','first_name','mid_name','passport_num','passport_date')
        ordering = ('last_name','first_name', 'mid_name',)

    birthdate = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    passport_num = models.CharField(blank=True, max_length=200, verbose_name="Номер паспорта РФ")
    passport_date = models.DateField(null=True, blank=True, verbose_name="Дата выдачи паспорта РФ")
    passport_issued_by = models.CharField(null=True, blank=True, max_length=50, verbose_name="Кем выдан паспорт РФ")
    international_passport = models.CharField(blank=True, max_length=200, verbose_name="Загранпаспорт")
    international_name = models.CharField(blank=True, max_length=200, verbose_name="Имя как в загранпаспорте")
    international_passport_date_of_expiry=models.DateField(null=True, blank=True, verbose_name="Срок действия загранпаспорта")
    phone = models.CharField(blank=True, max_length=50, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="e-mail")
    address = models.CharField(blank=True, max_length=200, verbose_name="Адрес")
    
    def get_warnings(self):
        warnings=[]
        if strip(self.last_name)=='' or strip(self.first_name) == '' or strip(self.mid_name)=='':
            warnings.append('Не заполнены ФИО')
        if strip(self.passport_num)=='' and strip(self.international_passport)=='':
            warnings.append('Не указан ни один документ')
        if self.birthdate == None:
            warnings.append('Не указана дата рождения')
        return warnings
        

class Contract(models.Model):
    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ('-contract_date',)
        
    contract_num = models.IntegerField(unique_for_month = "contract_date", verbose_name="Номер договора")
    contract_date = models.DateField(blank=True, null=True, verbose_name="Дата договора")
    manager = models.ForeignKey(Manager, on_delete = models.PROTECT, editable = False, blank=True, null=True, verbose_name="Менеджер")
    office = models.ForeignKey(Office, on_delete = models.PROTECT, editable = False, blank=True, null=True, verbose_name="Офис")
    client = models.ForeignKey(Tourist, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Клиент")
    status = models.ForeignKey(Status, on_delete = models.PROTECT, verbose_name="Статус")
    
    tour_begin_date = models.DateField(blank=True, verbose_name="Дата начала тура")
    tour_finish_date = models.DateField(blank=True, verbose_name="Дата окончания тура")
    contract_sum = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, verbose_name="Сумма контракта")
    signatory = models.ForeignKey(Manager, on_delete = models.PROTECT, related_name='contract_signatory', blank=True, null=True, verbose_name="Подписант")
    tourist_list = models.ManyToManyField(Tourist, blank=True, related_name='tourist_list', verbose_name="Список туристов") 
    
    tour_operator = models.ForeignKey(TourOperator, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Туроператор")
    resort =  models.ForeignKey(Resort, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Курорт")
    
    hotel_name = models.CharField(blank=True, max_length=200, verbose_name="Название отеля")
    hotel_begin_date = models.DateField(blank=True, null=True, verbose_name="Дата въезда в отель")
    hotel_finish_date = models.DateField(blank=True, null=True, verbose_name="Дата выезда из отеля")
    room_type = models.ForeignKey(RoomType, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Тип номера")
    board = models.ForeignKey(Board, on_delete = models.PROTECT, blank=True, null=True, verbose_name="Тип питания")
    
    transfer = models.BooleanField(blank=True, verbose_name="Включена перевозка наземным транспортом")
    #excursion = models.BooleanField(blank=True, verbose_name="Включена экскурсионная программа")
    excursions = models.TextField(blank=True, verbose_name="Включенные экскурсии")
    russian_guide = models.BooleanField(blank=True, verbose_name="Включена встреча и проводы с русскоговорящим гидом")
    visa_support = models.BooleanField(blank=True, verbose_name="Включена визовая поддержка")
    medical_insurance = models.BooleanField(blank=True, verbose_name="Включена медицинская страховка")
    non_departure_insurance = models.BooleanField(blank=True, verbose_name="Включена страховка от невыезда")
    visa_risk_insurance = models.BooleanField(blank=True, verbose_name="Включена страховка визового риска")
    
    confirm_date = models.DateField(blank=True, null=True, verbose_name="Дата подтверждения")
    doc_issue_date = models.DateField(blank=True, null=True, verbose_name="Дата выдачи документов")
    full_pay_date = models.DateField(blank=True, null=True, verbose_name="Дата полной оплаты")
    
    operator_sum = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, verbose_name="Сумма оператору")

    def save(self, *args, **kwargs):
        self.status=self.get_status()
        super(Contract, self).save(*args, **kwargs)
        
    def __str__(self):
        return 'Договор №' + self.contract_date.strftime('%m%y') + '-' + str(self.contract_num) + ' от ' + str(self.contract_date) + ' - ' + str(self.client)
    
    def is_printable(self):
        result = True
        if (self.get_prepayment_sum() <= 0):
            result = False
        return result
    
    def is_deletable(self):
        result=True
        if (self.status.status_name=='closed'
            or self.payment_set.count()>0): 
            result = False
        return result
    
    def is_editable (self):
        result=True
        if self.status.status_name=='closed':
            result = False
        return result

    def get_hotel_nights(self):
        return (self.hotel_finish_date-self.hotel_begin_date).days
    
    def get_prepayment_sum(self):
        prepayment_sum = self.payment_set.all().order_by('payment_date').first().payment_sum if self.payment_set.all() else 0
        return prepayment_sum
    
    def get_postpayment_sum(self):
        return self.contract_sum - self.get_prepayment_sum()
    
    def get_all_payments_sum(self):
        total_sum = self.payment_set.all().aggregate(models.Sum('payment_sum'))['payment_sum__sum'] if self.payment_set.all() else 0
        return total_sum
        
    def get_remain_payment_sum(self):
        return self.contract_sum - self.get_all_payments_sum()
    
    def get_contract_sum_string(self):
        rub = ((u'рубль', u'рубля', u'рублей'), 'm')
        kop = ((u'копейка', u'копейки', u'копеек'), 'f')
        sum_arr = modf(self.contract_sum)
        sum_str = num2text(sum_arr[1],rub)+' '+num2text(sum_arr[0]*100,kop)
        return sum_str
    
    def filled_fully(self):
        result=True
        if(
            self.contract_date == None
            or self.tour_begin_date == None
            or self.tour_finish_date == None
            or self.hotel_begin_date == None
            or self.hotel_finish_date == None
            
            or self.client == None
            or self.tour_operator == None
            or self.resort == None
            or self.tourist_list.count()<1
            or self.hotel_name == ''
            or self.room_type == None
            or self.board == None
            
            or self.contract_sum <= 0
            ):
            result=False
        
        return result    
    
    def get_status(self):
        contract_class = None
        if self.filled_fully() == True:
            contract_class = "signed"
            if self.confirm_date:
                contract_class = "confirmed"
                if self.get_all_payments_sum() == self.contract_sum:
                    contract_class = "fully_paid"
                    if self.doc_issue_date:
                        contract_class = "doc_isssued"
        
        
        
        #if self.filled_fully() == False:
        #    contract_class = "signed"
        #    if self.confirm_date:
        #        contract_class = "confirmed"
        #else:
        #    if self.get_all_payments_sum() < self.contract_sum:
        #        contract_class = "signed"
        #    elif self.get_all_payments_sum() == self.contract_sum:
        #        contract_class = "paid"
        #        if self.tour_finish_date < timezone.datetime.now().date():
        #            contract_class = "closed"
        return Status.objects.get(status_name=contract_class)
    
    #def is_important(self):
    #    if (self.confirm_date == None
    #        or (self.confirm_date and self.tour_begin_date-timezone.today()<=14) 
    #        or self.doc_issue_date == None):
    #        result=True
    #    return result   
    
    def get_warnings(self):
        warnings=[]
        #warnings.append('Шо-та не так')
        #warnings.append('Шо-та ваще не так')
        #warnings.append(self.client.get_warnings())
        
        #for tourist in self.tourist_list:
        #    warnings.append(tourist.get_warnings())
        
        return warnings 
        

class PaymentMethod(models.Model):
    class Meta:
        verbose_name = "Форма оплаты"
        verbose_name_plural = "Формы оплаты"
    
    method_name = models.CharField(max_length=200, verbose_name="Название")
    method_full_name = models.CharField(max_length=200, verbose_name="Полное наименование")
    
    def __str__(self):
        return (self.method_full_name)


class Payment(models.Model):
    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
    
    contract = models.ForeignKey(Contract, on_delete = models.PROTECT, verbose_name="Договор")
    manager = models.ForeignKey(Manager, on_delete = models.PROTECT, editable = False, verbose_name="Менеджер")
    office = models.ForeignKey(Office, on_delete = models.PROTECT, editable = False, verbose_name="Офис")
    payment_method = models.ForeignKey(PaymentMethod, on_delete = models.PROTECT, verbose_name="Форма оплаты")
    payment_date = models.DateTimeField(auto_now_add=True, editable = False, verbose_name="Дата внесения")
    payment_sum = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Сумма платежа")
    
    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)
        #self.contract.status=self.contract.get_status()
        self.contract.save(update_fields=['status'])
    
    def delete(self, *args, **kwargs):
        super(Payment, self).delete(*args, **kwargs)
        #self.contract.status=self.contract.get_status()
        self.contract.save(update_fields=['status'])
        
    
    def is_deletable(self):
        result=True
        if self.contract.status.status_name=='closed':
            result = False
        return result
    
    def __str__(self):
        #return 'Платеж по договору '+str(self.contract)+' на сумму '+str(self.payment_sum)
        return 'Платеж по договору '+str(self.contract)+' на сумму '+str(self.payment_sum)
    
