import django_filters

from .models import Quant
from ltb.models import LTBType, LTBNumber, LTBEditionNumber


class QuantFilter(django_filters.FilterSet):
    """
    TODO: Docstring
    """
    ON_STOCK_CHOICES = {
        (True, 'Original'),
        (False, 'Nachdruck')
    }
    READ_CHOICES = {
        (True, 'Gelesen'),
        (False, 'Ungelesen')
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
    first_edition = django_filters.ChoiceFilter(label="Druck",
                                                choices=ON_STOCK_CHOICES,
                                                method='filter_data',
                                                empty_label="Alle")
    read = django_filters.ChoiceFilter(label='Gelesen',
                                       choices=READ_CHOICES,
                                       method='filter_data',
                                       empty_label="Alle")

    class Meta:
        """
        TODO: Docstring
        """
        model = Quant
        fields = ['complete_name', 'number', 'edition', 'first_edition', 'read']

    @staticmethod
    def filter_data(queryset, name, value):
        """
        TODO: Docstring

        :param queryset:
        :param name:
        :param value:
        :return:
        """
        if name == 'number':
            queryset = queryset.filter(book__ltb_edition__ltb_number_set__ltb_number=value)
        if name == 'edition':
            queryset = queryset.filter(book__ltb_edition__ltb_edition_number=value)
        if name == 'first_edition':
            queryset = queryset.filter(is_first_edition=value)
        if name == 'read':
            queryset = queryset.filter(book__is_read=value)
        return queryset


class QuantCompleteFilter(QuantFilter):
    """
    TODO: Docstring
    """
    type = django_filters.ModelChoiceFilter(label='Typ',
                                            queryset=LTBType.objects.all(),
                                            method='filter_data',
                                            empty_label="Alle")

    class Meta:
        """
        TODO: Docstring
        """
        model = Quant
        fields = ['complete_name', 'number', 'edition', 'first_edition', 'read', 'type']

    @staticmethod
    def filter_data(queryset, name, value):
        """
        TODO: Docstring

        :param queryset:
        :param name:
        :param value:
        :return:
        """
        queryset = QuantFilter.filter_data(queryset, name, value)
        if name == 'type':
            queryset = queryset.filter(book__ltb_edition__ltb_number_set__ltb_type=value)
        return queryset
