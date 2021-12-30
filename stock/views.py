from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.views.generic import DetailView
from django_filters.views import FilterView
from django.views.generic.edit import FormView

from .forms import AddBookForm, FindNumberForm

from .models import Quant
from ltb.models import LTBType

from .filters import QuantFilter


class QuantList(FilterView):
    """
    TODO: Docstring
    """
    model = Quant
    filterset_class = QuantFilter
    template_name = 'stock/list.html'
    paginate_by = 30

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        s_type = self.kwargs.get('s_type')
        if s_type == "all":
            queryset = Quant.objects.all()
        else:
            ltb_type = LTBType.objects.filter(code=s_type.upper()).get()
            queryset = Quant.objects.filter(book__ltb_edition__ltb_number_set__ltb_type=ltb_type).all()
        return queryset

    def get_paginate_by(self, queryset):
        """
        TODO: Docstring

        :param queryset:
        :return:
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class AddBook(FormView):
    """
    TODO: Docstring
    """
    template_name = 'stock/add_book.html'
    form_class = AddBookForm
    success_url = '/stock/book/add'

    def form_valid(self, form):
        """
        TODO: Docstring

        :param form:
        :return:
        """
        if self.request.user and self.request.user.has_perm('stock.add_quant_on_site'):
            quant = form.save()
            messages.success(self.request,
                             f"\"{quant.book.number} {quant.book.type} - {quant.book.complete_name}\" wurde hinzugefügt")
            result = super().form_valid(form)
        else:
            messages.error(self.request, "Keine Berechtigung")
            result = super().form_valid(form)
        return result


class FindNumber(FormView):
    """
    TODO: Docstring
    """
    template_name = 'stock/find_number.html'
    form_class = FindNumberForm
    success_url = '/stock/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ltb_type = "all"
        self.ltb_number = ""

    def form_valid(self, form):
        """
        TODO: Docstring

        :param form:
        :return:
        """

        self.ltb_type = form.cleaned_data['ltb_type']
        self.ltb_number = form.cleaned_data['ltb_number']

        result = super().form_valid(form)
        return result

    def get_success_url(self):
        """
        TODO: Docstring

        :return:
        """
        url = super(FindNumber, self).get_success_url()
        url += f"{self.ltb_type}"
        url += f"?number={self.ltb_number}"
        return url
