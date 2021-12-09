from django.contrib import admin
from .models import Quant


@admin.register(Quant)
class StockQuantAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    list_display = ('book', 'is_first_edition')
    ordering = ('book',)
