from django.contrib import admin
from .models import Portfolio, Asset, Holding, Price, Weight

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Puedes agregar más campos si tienes

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Holding)
class HoldingAdmin(admin.ModelAdmin):
    list_display = ('id', 'portfolio', 'asset', 'quantity')
    list_filter = ('portfolio', 'asset')

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'date', 'price')
    list_filter = ('asset', 'date')

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('id', 'portfolio', 'asset', 'weight')
    list_filter = ('portfolio', 'asset')