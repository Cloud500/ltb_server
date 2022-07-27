from django.contrib import admin

from .models import Person
from .admin_forms import PersonForm


@admin.action(description='Fetch Person Data')
def get_person_data(modeladmin, request, queryset):
    person: Person
    for person in queryset:
        person.fetch_data()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    TODO: Docstring
    """
    form = PersonForm

    list_display = ('name', 'type', 'url')
    search_fields = ('name', 'type', 'description')
    list_filter = ('type',)
    ordering = ('name',)
    actions = [get_person_data, ]
