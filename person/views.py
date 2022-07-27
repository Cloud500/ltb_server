from django_filters.views import FilterView
from django.views.generic import DetailView

from .models import Person
from .filters import PersonFilter


class RealPersonList(FilterView):
    """
    TODO: Docstring
    """
    model = Person
    filterset_class = PersonFilter
    template_name = 'person/real/list.html'
    paginate_by = 30

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        queryset = Person.objects.filter(type="real").all()

        return queryset

    def get_paginate_by(self, queryset):
        """
        TODO: Docstring

        :param queryset:
        :return:
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class FictionalPersonList(FilterView):
    """
    TODO: Docstring
    """
    model = Person
    filterset_class = PersonFilter
    template_name = 'person/fictional/list.html'
    paginate_by = 32

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        queryset = Person.objects.filter(type="fictional").all()

        return queryset

    def get_paginate_by(self, queryset):
        """
        TODO: Docstring

        :param queryset:
        :return:
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class RealPersonDetail(DetailView):
    """
    Detail view for the LTB model.

    Processes the GET and POST requests and evaluate his forms
    """
    model = Person
    template_name = 'person/real/detail.html'


class FictionalPersonDetail(DetailView):
    """
    Detail view for the LTB model.

    Processes the GET and POST requests and evaluate his forms
    """
    model = Person
    template_name = 'person/fictional/detail.html'
