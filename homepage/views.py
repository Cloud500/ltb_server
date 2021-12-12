from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic import TemplateView

from ltb.models import LTBNumberSet, LTBType
from .forms import LoginForm
from .news_scraper import NewsScraper


class Index(TemplateView):
    """
        TODO: Docstring
    """
    template_name = 'homepage/index.html'

    @staticmethod
    def _type_overview(all_number_set, ltb_type):
        """
        TODO: Docstring

        :param all_number_set:
        :param ltb_type:
        :return:
        """
        type_number_query_set = all_number_set.filter(ltb_type=ltb_type)
        number_query_exist = type_number_query_set.filter(editions__ltbs__quants__isnull=False).distinct()
        number_query_missing = type_number_query_set.exclude(id__in=number_query_exist.values_list('id', flat=True))
        missing_numbers = list(
            map(lambda number: str(number).zfill(3),
                list(number_query_missing.order_by('ltb_number__number').values_list('ltb_number__number', flat=True))))

        return {
            'name': ltb_type.name,
            'code': ltb_type.code,
            'count_exists': len(number_query_exist),
            'count_all': len(type_number_query_set),
            'missing_numbers': missing_numbers,
        }

    def _get_overview_data(self):
        """
        TODO: Docstring

        :return:
        """
        data = {}
        all_number_set = LTBNumberSet.objects.all()

        for ltb_type in LTBType.objects.all():
            data[ltb_type.code] = self._type_overview(all_number_set, ltb_type)

        return data

    def get_context_data(self, **kwargs):
        """
        TODO: Docstring

        :param kwargs:
        :return:
        """
        if 'login_form' not in kwargs:
            kwargs['login_form'] = LoginForm()
        if 'overview_data' not in kwargs:
            kwargs['overview_data'] = self._get_overview_data()
        if 'news_data' not in kwargs:
            kwargs['news_data'] = NewsScraper().news
        return kwargs

    def get(self, request, *args, **kwargs):
        """
        TODO: Docstring

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        result = super(Index, self).get(request)
        return result

    def post(self, request):
        """
        TODO: Docstring

        :param request:
        :return:
        """
        if 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                cleaned_data = login_form.cleaned_data
                user = authenticate(request,
                                    username=cleaned_data['username'],
                                    password=cleaned_data['password'])
                if user is not None and user.is_active:
                    login(request, user)

        if 'logout' in request.POST:
            logout(request)

        result = super(Index, self).get(request)
        return result
