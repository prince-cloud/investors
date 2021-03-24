from django.contrib import admin
from .models import Investor
# Register your models here.

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'phone', 'country_to_invest', 'state', 'city', 'zip_code',)
    list_filter = ('country_to_invest', 'state', 'city')