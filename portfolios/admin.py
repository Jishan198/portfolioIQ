from django.contrib import admin
from .models import Portfolio, Holding

class HoldingInline(admin.TabularInline):
    model = Holding
    extra = 1

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    inlines = [HoldingInline]

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'portfolio', 'quantity', 'buy_price', 'buy_date')
    list_filter = ('ticker', 'buy_date')
# Register your models here.
