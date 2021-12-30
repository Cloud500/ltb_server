import django_filters

from .models import LTB, LTBType, LTBNumber, LTBEditionNumber


class LTBFilter(django_filters.FilterSet):
    """
    TODO: Docstring
    """
    ON_STOCK_CHOICES = {
        (True, 'In Besitz'),
        (False, 'Nicht in Besitz')
    }
    READ_CHOICES = {
        (True, 'Gelesen'),
        (False, 'Ungelesen')
    }

    complete_name = django_filters.CharFilter(label='Name',
                                              lookup_expr='icontains')
    number = django_filters.NumberFilter(label='Nummer',
                                         method='filter_data')

    edition = django_filters.ModelChoiceFilter(label='Auflage',
                                               queryset=LTBEditionNumber.objects.all(),
                                               method='filter_data',
                                               empty_label="Alle")
    on_stock = django_filters.ChoiceFilter(label='Besitz',
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
        model = LTB
        fields = ['complete_name', 'number', 'edition', 'read']

    @staticmethod
    def filter_data(queryset, name, value):
        """
        TODO: Docstring

        :param queryset:
        :param name:
        :param value:
        :return:
        """
        if name == 'on_stock':
            if value:
                id_list = list(LTB.in_stock.values_list('id', flat=True))
                queryset = queryset.filter(id__in=id_list)
            elif not value:
                id_list = list(LTB.not_in_stock.values_list('id', flat=True))
                queryset = queryset.filter(id__in=id_list)
        if name == 'number':
            queryset = queryset.filter(ltb_edition__ltb_number_set__ltb_number__number=value)
        if name == 'edition':
            queryset = queryset.filter(ltb_edition__ltb_edition_number=value)
        if name == 'read':
            queryset = queryset.filter(is_read=value)
        return queryset
