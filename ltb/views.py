from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django_filters.views import FilterView

from .models import LTB, LTBType
from .filters import LTBFilter
from .forms import AddBookForm


class LTBList(FilterView):
    """
    TODO: Docstring
    """
    model = LTB
    filterset_class = LTBFilter
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
    Detail view for the LTB model.

    Processes the GET and POST requests and evaluate his forms
    """
    model = LTB
    template_name = 'ltb/detail.html'

    def get_context_data(self, **kwargs: dict) -> dict:
        """
        Add data to tie context.

        Add the follow things:
            add_book_form => A Form to add a new Book to the Inventory

        :param kwargs: Context arguments.
        :type kwargs: dict
        :return: Updated context arguments.
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        if 'add_book_form' not in context:
            context['add_book_form'] = AddBookForm()
        return context

    def evaluate_read_book_form(self):
        """
        Evaluate the read_book 'form'

        TODO: Make a real Form to this
        """
        slug = self.kwargs.get('slug')
        ltb = get_object_or_404(LTB, slug=slug)
        if ltb.is_read:
            ltb.is_read = False
        else:
            ltb.is_read = True
        ltb.save()

    def evaluate_add_book_form(self, request: WSGIRequest):
        """
        Evaluate the add_book_form form

        :param request: Request data
        :type request: WSGIRequest
        """
        data = request.POST.copy()
        data['slug'] = self.kwargs.get('slug')

        add_book = AddBookForm(data)
        if add_book.is_valid():
            add_book.save()

    def post(self, request: WSGIRequest, *args: tuple, **kwargs: dict) -> TemplateResponse:
        """
        Processes the POST request of the view

        :param request: Request data
        :type request: WSGIRequest
        :param args: Custom arguments
        :type args: tuple
        :param kwargs: Path arguments
        :type kwargs: dict
        :return: HTTP Response
        :rtype: TemplateResponse
        """
        if request.POST.get('read_book'):
            self.evaluate_read_book_form()

        if request.POST.get('add_book'):
            self.evaluate_add_book_form(request)
        data = self.get(request, *args, **kwargs)
        return data
