from django_filters.views import FilterView
from django.views.generic import DetailView

from .models import Story
from .filters import StoryFilter


class StoryList(FilterView):
    """
    TODO: Docstring
    """
    model = Story
    filterset_class = StoryFilter
    template_name = 'story/list.html'
    paginate_by = 30

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        queryset = Story.objects.all()

        return queryset

    def get_paginate_by(self, queryset):
        """
        TODO: Docstring

        :param queryset:
        :return:
        """
        return self.request.GET.get('paginate_by', self.paginate_by)


class StoryDetail(DetailView):
    """
    TODO: Docstring
    """
    model = Story
    template_name = 'story/detail.html'
