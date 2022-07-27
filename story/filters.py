import django_filters
from django.forms import DateInput

from .models import Story, Genre
from ltb.models import LTBEdition, LTBType


class StoryFilter(django_filters.FilterSet):
    """
    TODO: Docstring
    """
    title = django_filters.CharFilter(label='Titel',
                                      lookup_expr='icontains')
    code = django_filters.CharFilter(label='Code',
                                     lookup_expr='icontains')
    original_title = django_filters.CharFilter(label='Originaltitel',
                                               lookup_expr='icontains')
    origin = django_filters.CharFilter(label='Herkunft',
                                       lookup_expr='icontains')

    date_from = django_filters.DateFilter(label='Datum von',
                                          method='filter_data',
                                          widget=DateInput(attrs={'type': 'date'}))
    date_to = django_filters.DateFilter(label='Datum bis',
                                        method='filter_data',
                                        widget=DateInput(attrs={'type': 'date'}))

    edition = django_filters.CharFilter(label='Buchtitel',
                                        method='filter_data',
                                        lookup_expr='icontains')

    type = django_filters.ModelChoiceFilter(label='Typ',
                                            queryset=LTBType.objects.all(),
                                            method='filter_data',
                                            empty_label="Alle")

    genre = django_filters.ModelMultipleChoiceFilter(label='Genre',
                                                     queryset=Genre.objects.all(),
                                                     conjoined=True)

    class Meta:
        """
        TODO: Docstring
        """
        model = Story
        fields = ['title', 'code', 'original_title', 'origin', 'date_from', 'date_to', 'edition', 'type']

    @staticmethod
    def filter_data(queryset, name, value):
        """
        TODO: Docstring

        :param queryset:
        :param name:
        :param value:
        :return:
        """
        if name == 'date_from':
            queryset = queryset.filter(date__gte=value).all()

        if name == 'date_to':
            queryset = queryset.filter(date__lte=value).all()

        if name == 'edition':
            editions = LTBEdition.objects.filter(title__icontains=value).all()
            queryset = queryset.filter(LTBEditionStory__ltb_edition__in=editions).distinct()
        if name == 'type':
            queryset = queryset.filter(LTBEditionStory__ltb_edition__ltb_number_set__ltb_type=value).all()

        return queryset
