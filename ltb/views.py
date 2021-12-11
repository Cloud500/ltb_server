from django.views import View
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import DetailView
from django_filters.views import FilterView

from .models import LTB, LTBType
from .filters import LTBFilter, LTBCompleteFilter


class LTBList(FilterView):
    """
    TODO: Docstring
    """
    model = LTB
    filterset_class = LTBCompleteFilter
    template_name = 'ltb/list.html'
    paginate_by = 30

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        s_type = self.kwargs.get('s_type')
        if s_type == "all":
            queryset = LTB.objects.all()
        else:
            ltb_type = LTBType.objects.filter(code=s_type.upper()).get()
            queryset = LTB.objects.filter(ltb_edition__ltb_number_set__ltb_type=ltb_type).all()  # TODO: Refactor
        return queryset

    def get_paginate_by(self, queryset):
        """
        TODO: Docstring

        :param queryset:
        :return:
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class LTBDetail(DetailView):
    """
    TODO: Docstring
    """
    model = LTB
    template_name = 'ltb/detail.html'

    def post(self, request, *args, **kwargs):
        """
        TODO: Docstring

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.POST.get('read_book'):
            slug = self.kwargs.get('slug')
            ltb = get_object_or_404(LTB, slug=slug)
            if ltb.is_read:
                ltb.is_read = False
            else:
                ltb.is_read = True
            ltb.save()
        response = self.get(request, *args, **kwargs)
        return response
