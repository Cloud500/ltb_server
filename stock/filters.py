import django_filters

from .models import Quant
from ltb.models import LTBType, LTBNumber, LTBEditionNumber


class QuantFilter(django_filters.FilterSet):
    ON_STOCK_CHOICES = {
        (True, 'In Besitz'),
        (False, 'Nicht in Besitz')
    }

    complete_name = django_filters.CharFilter(label='Name',
                                              lookup_expr='icontains')
    number = django_filters.ModelChoiceFilter(label='Nummer',
                                              queryset=LTBNumber.objects.all(),
                                              method='filter_data',
                                              empty_label="Alle")
    edition = django_filters.ModelChoiceFilter(label='Auflage',
                                               queryset=LTBEditionNumber.objects.all(),
                                               method='filter_data',
                                               empty_label="Alle")

    class Meta:
        model = Quant
        fields = ['complete_name', 'number', 'edition']

    @staticmethod
    def filter_data(queryset, name, value):
        if name == 'number':
            queryset = queryset.filter(book__ltb_edition__ltb_number_set__ltb_number=value)
        if name == 'edition':
            queryset = queryset.filter(book__ltb_edition__ltb_edition_number=value)
        return queryset


class QuantCompleteFilter(QuantFilter):
    type = django_filters.ModelChoiceFilter(label='Typ',
                                            queryset=LTBType.objects.all(),
                                            method='filter_data',
                                            empty_label="Alle")

    class Meta:
        model = Quant
        fields = ['complete_name', 'number', 'edition', 'type']

    @staticmethod
    def filter_data(queryset, name, value):
        queryset = QuantFilter.filter_data(queryset, name, value)
        if name == 'type':
            queryset = queryset.filter(book__ltb_edition__ltb_number_set__ltb_type=value)
        return queryset
