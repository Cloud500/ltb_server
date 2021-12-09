from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import LTB, LTBType
from .filters import LTBFilter, LTBCompleteFilter


def ltb_list(request, s_type: str):
    """
    TODO: Docstring

    :param request:
    :param s_type:
    :return:
    """
    paginate_by = request.GET.get('paginate_by', 30) or 30
    if s_type == "all":
        ltbs = LTB.objects.all()
        filter_qs = LTBCompleteFilter(request.GET, queryset=ltbs)
    else:
        ltb_type = LTBType.objects.filter(code=s_type.upper()).get()
        ltbs = LTB.objects.filter(ltb_edition__ltb_number_set__ltb_type=ltb_type).all()  # TODO: Refactor
        filter_qs = LTBFilter(request.GET, queryset=ltbs)

    paginator = Paginator(filter_qs.qs, paginate_by)
    page = request.GET.get('page')
    form = filter_qs.form

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request,
                  'ltb/list.html',
                  {'page': page,
                   'form': form,
                   'books': books})


def book_detail(request, slug: str):
    """
    TODO: Docstring

    :param request:
    :param slug:
    :return:
    """
    book = get_object_or_404(LTB, slug=slug)

    return render(request,
                  'ltb/detail.html',
                  {'book': book})
