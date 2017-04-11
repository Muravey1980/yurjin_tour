from django.contrib import admin

# Register your models here.
from .models import Country, Resort, TourOperator, RoomType, Board, Office, Manager, Tourist, Status, Contract, TourAgency, Payment, PaymentMethod

admin.site.register(Country)
admin.site.register(Resort)
admin.site.register(TourOperator)
admin.site.register(RoomType)
admin.site.register(Board)
admin.site.register(TourAgency)
admin.site.register(Office)
admin.site.register(Manager)
admin.site.register(Tourist)
admin.site.register(Status)
admin.site.register(Contract)
admin.site.register(Payment)
admin.site.register(PaymentMethod)
