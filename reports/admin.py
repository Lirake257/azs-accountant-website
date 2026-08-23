from django.contrib import admin
from .models import AccountantProfile, FuelReport

@admin.register(AccountantProfile)
class AccountantProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'station_name')
    search_fields = ('user__username', 'station_name')

@admin.register(FuelReport)
class FuelReportAdmin(admin.ModelAdmin):
    list_display = ('accountant', 'date', 'ai92_sold', 'cash_sales')
    list_filter = ('date', 'accountant')
    search_fields = ('accountant__username',)