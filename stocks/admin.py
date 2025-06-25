from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("symbol", "name", "price","last_updated")  # 🆕 Added field
    search_fields = ("symbol", "name")
    list_filter = ("symbol",)
