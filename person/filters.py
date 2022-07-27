import django_filters

from .models import Person


class PersonFilter(django_filters.FilterSet):
    """
    TODO: Docstring
    """
    name = django_filters.CharFilter(label='Name',
                                     lookup_expr='icontains')

    class Meta:
        """
        TODO: Docstring
        """
        model = Person
        fields = ['name', ]

    # @staticmethod
    # def filter_data(queryset, name, value):
    #     """
    #     TODO: Docstring
    #
    #     :param queryset:
    #     :param name:
    #     :param value:
    #     :return:
    #     """
    #     if name == 'on_stock':
    #         if value:
    #             id_list = list(LTB.in_stock.values_list('id', flat=True))
    #             queryset = queryset.filter(id__in=id_list)
    #         elif not value:
    #             id_list = list(LTB.not_in_stock.values_list('id', flat=True))
    #             queryset = queryset.filter(id__in=id_list)
    #     if name == 'number':
    #         queryset = queryset.filter(ltb_edition__ltb_number_set__ltb_number__number=value)
    #     if name == 'edition':
    #         queryset = queryset.filter(ltb_edition__ltb_edition_number=value)
    #     if name == 'read':
    #         queryset = queryset.filter(is_read=value)
    #     return queryset
