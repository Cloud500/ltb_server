import django_filters

from .models import LTB, LTBType, LTBNumber, LTBEditionNumber


class LTBFilter(django_filters.FilterSet):
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
    on_stock = django_filters.ChoiceFilter(label='Besitz',
                                           choices=ON_STOCK_CHOICES,
                                           method='filter_data',
                                           empty_label="Alle")

    class Meta:
        model = LTB
        fields = ['complete_name', 'number', 'edition']

    @staticmethod
    def filter_data(queryset, name, value):
        if name == 'on_stock':
            if value:
                id_list = list(LTB.in_stock.values_list('id', flat=True))
                queryset = queryset.filter(id__in=id_list)
            elif not value:
                id_list = list(LTB.not_in_stock.values_list('id', flat=True))
                queryset = queryset.filter(id__in=id_list)
        if name == 'number':
            queryset = queryset.filter(ltb_edition__ltb_number_set__ltb_number=value)
        if name == 'edition':
            queryset = queryset.filter(ltb_edition__ltb_edition_number=value)
        return queryset


class LTBCompleteFilter(LTBFilter):
    type = django_filters.ModelChoiceFilter(label='Typ',
                                            queryset=LTBType.objects.all(),
                                            method='filter_data',
                                            empty_label="Alle")

    class Meta:
        model = LTB
        fields = ['complete_name', 'number', 'edition', 'type', 'on_stock']

    @staticmethod
    def filter_data(queryset, name, value):
        queryset = LTBFilter.filter_data(queryset, name, value)
        if name == 'type':
            queryset = queryset.filter(ltb_edition__ltb_number_set__ltb_type=value)
        return queryset
