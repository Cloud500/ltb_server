from datetime import timedelta, timezone, datetime

from django.contrib import admin
from .admin_forms import LTBTypeForm, LTBNumberForm, LTBNumberSetForm, LTBEditionNumberForm, LTBEditionForm, LTBForm
from .models import LTBType, LTBNumber, LTBNumberSet, LTBEditionNumber, LTBEdition, LTB


@admin.action(description='Fetch next number')
def get_next_number(modeladmin, request, queryset):
    """
    TODO: Docstring

    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    for ltb_type in queryset:
        ltb_type.fetch_next_number()


@admin.action(description='Create All Books for this Type')
def create_books(modeladmin, request, queryset):
    """
    TODO: Docstring

    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    for type in queryset:
        type.create_books()


@admin.register(LTBType)
class LTBTypeAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBTypeForm

    list_display = ('name', 'code', 'auto_url', 'auto_fetch', 'type_url')
    search_fields = ('name', 'code')
    ordering = ('code',)
    actions = [create_books, get_next_number]


@admin.action(description='Create Editions for this Numbers')
def create_editions(modeladmin, request, queryset):
    """
    TODO: Docstring

    :param modeladmin:
    :param request:
    :param queryset:
    :return:
    """
    for number in queryset:
        if number.url:
            number.create_editions()


@admin.register(LTBNumber)
class LTBNumberAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBNumberForm

    list_display = ('number',)
    search_fields = ('number',)
    ordering = ('number',)


@admin.register(LTBNumberSet)
class LTBNumberSetAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBNumberSetForm

    list_display = ('ltb_number', 'ltb_type', 'url')
    search_fields = ('ltb_number', 'ltb_type')
    list_filter = ('ltb_type', 'ltb_number')
    ordering = ('ltb_number',)

    actions = [create_editions, ]


@admin.register(LTBEditionNumber)
class LTBEditionNumberAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBEditionNumberForm

    list_display = ('number',)
    search_fields = ('number',)
    ordering = ('number',)


@admin.register(LTBEdition)
class LTBEditionAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBEditionForm

    list_display = ('ltb_number_set', 'ltb_edition_number', 'title')
    search_fields = ('ltb_number_set__ltb_number__number', 'ltb_edition_number__number', 'title')
    list_filter = ('ltb_edition_number', 'ltb_number_set__ltb_type')
    ordering = ('ltb_number_set', 'ltb_edition_number')


@admin.register(LTB)
class LTBAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = LTBForm

    list_display = ('ltb_edition', 'name', 'sort', 'is_read')
    search_fields = ('ltb_edition', 'name',)
    ordering = ('ltb_edition', 'sort')
