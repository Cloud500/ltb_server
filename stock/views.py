from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import AddBookForm

from .models import Quant
from ltb.models import LTBType

from .filters import QuantFilter, QuantCompleteFilter


def quant_list_type(request, s_type: str):
    paginate_by = request.GET.get('paginate_by', 30) or 30
    if s_type == "all":
        quants = Quant.objects.all()
        filter_qs = QuantCompleteFilter(request.GET, queryset=quants)
    else:
        ltb_type = LTBType.objects.filter(code=s_type.upper()).get()
        quants = Quant.objects.filter(book__ltb_edition__ltb_number_set__ltb_type=ltb_type).all()
        filter_qs = QuantFilter(request.GET, queryset=quants)

    paginator = Paginator(filter_qs.qs, paginate_by)
    page = request.GET.get('page')
    form = filter_qs.form

    try:
        quants = paginator.page(page)
    except PageNotAnInteger:
        quants = paginator.page(1)
    except EmptyPage:
        quants = paginator.page(paginator.num_pages)

    return render(request,
                  'stock/list.html',
                  {'page': page,
                   'form': form,
                   'quants': quants})


def add_book(request):
    user = request.user
    if request.method == "POST":
        form = AddBookForm(data=request.POST)
        if user and user.has_perm('stock.add_quant_on_site'):
            if form.is_valid():
                message = form.save()
                return render(request,
                              'stock/add_book.html',
                              {'message': message,
                               'form': form})
        else:
            message = {
                'success': False,
                'message': f"Sie sind nicht berechtigt Bücher zum Inventar hinzuzufügen"}

            return render(request,
                          'stock/add_book.html',
                          {'message': message,
                           'form': form})

    else:
        form = AddBookForm(initial={'first_edition': False})

    return render(request,
                  'stock/add_book.html',
                  {'form': form})
