from django.contrib import admin

from .admin_forms import LTBTypeForm, LTBNumberNumberForm, LTBNumberSetForm, LTBEditionNumberForm, LTBEditionForm, \
    LTBSpecialEditionForm
from .models import LTBType, LTBNumberNumber, LTBNumberSet, LTBEditionNumber, LTBEdition, LTBSpecialEdition


@admin.action(description='Create All Books for this Type')
def create_books(modeladmin, request, queryset):
    for type in queryset:
        type.create_books()


@admin.register(LTBType)
class LTBTypeAdmin(admin.ModelAdmin):
    form = LTBTypeForm

    list_display = ('name', 'code', 'auto_url', 'type_url')
    search_fields = ('name', 'code')
    ordering = ('code',)
    actions = [create_books, ]


@admin.action(description='Create Editions for this Numbers')
def create_editions(modeladmin, request, queryset):
    for number in queryset:
        if number.url:
            number.create_editions()


@admin.register(LTBNumberNumber)
class LTBNumberNumberAdmin(admin.ModelAdmin):
    form = LTBNumberNumberForm

    list_display = ('number',)
    search_fields = ('number',)
    ordering = ('number',)


@admin.register(LTBNumberSet)
class LTBNumberSetAdmin(admin.ModelAdmin):
    form = LTBNumberSetForm

    list_display = ('ltb_number_number', 'ltb_type', 'url')
    search_fields = ('ltb_number_number', 'ltb_type')
    list_filter = ('ltb_type', 'ltb_number_number')
    ordering = ('ltb_number_number',)

    actions = [create_editions, ]


@admin.register(LTBEditionNumber)
class LTBEditionNumberAdmin(admin.ModelAdmin):
    form = LTBEditionNumberForm

    list_display = ('number',)
    search_fields = ('number',)
    ordering = ('number',)


@admin.register(LTBEdition)
class LTBEditionAdmin(admin.ModelAdmin):
    form = LTBEditionForm

    list_display = ('ltb_number_set', 'ltb_edition_number', 'title')
    search_fields = ('ltb_number_set__ltb_number_number__number', 'ltb_edition_number__number', 'title')
    list_filter = ('ltb_edition_number', 'ltb_number_set__ltb_type')
    ordering = ('ltb_number_set', 'ltb_edition_number')


@admin.register(LTBSpecialEdition)
class LTBSpecialEditionAdmin(admin.ModelAdmin):
    form = LTBSpecialEditionForm

    list_display = ('ltb_edition', 'name', 'sort')
    search_fields = ('ltb_edition', 'name',)
    ordering = ('ltb_edition', 'sort')
