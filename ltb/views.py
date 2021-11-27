from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import LTBSpecialEdition, LTBType
from .filters import BookFilter, BookCompleteFilter


def book_list_type(request, s_type: str):
    paginate_by = request.GET.get('paginate_by', 30) or 30
    if s_type == "all":
        special_editions = LTBSpecialEdition.objects.all()
        filter_qs = BookCompleteFilter(request.GET, queryset=special_editions)
    else:
        ltb_type = LTBType.objects.filter(code=s_type.upper()).get()
        special_editions = LTBSpecialEdition.objects.filter(ltb_edition__ltb_number_set__ltb_type=ltb_type).all()
        filter_qs = BookFilter(request.GET, queryset=special_editions)

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
    book = get_object_or_404(LTBSpecialEdition, slug=slug)

    return render(request,
                  'ltb/detail.html',
                  {'book': book})
