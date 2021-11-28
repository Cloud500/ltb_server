from django import template
from django.db.models import Count
from django.db.models import F

from stock.models import Quant
from ltb.models import LTB, LTBType, LTBNumberSet, LTBEdition

register = template.Library()


def get_all1_numbers(ltb_type):
    number_query_all = LTBNumberSet.objects.filter(ltb_type=ltb_type).all()
    return len(number_query_all)


def get_missing_books(ltb_type):
    existing_number_ids = list(
        Quant.objects.values_list('book__ltb_edition__ltb_number_set__id', flat=True))
    number_query_missing = LTBNumberSet.objects.exclude(id__in=existing_number_ids).filter(ltb_type=ltb_type).all()
    data = {}
    for number in number_query_missing:
        data[str(number.ltb_number)] = {}
        for edition in number.editions.all():
            data[str(number.ltb_number)][str(edition.ltb_edition_number)] = []
            for book in edition.ltbs.all():
                if book.name:
                    data[str(number.ltb_number)][str(edition.ltb_edition_number)].append(book.name)

    return data


@register.simple_tag()
def get_dict_value(data, key):
    if isinstance(data, dict):
        try:
            return data[key]
        except KeyError:
            return None
    return None


def format_all_missing_data(list):
    """
    TODO: Implementieren
    test = list(
            number_query_missing.values_list(
                                'ltb_number__number',
                                'editions__ltb_edition_number__number',
                                'editions__ltbs__name',
                                'editions__title'))
    """
    master_data = {}
    for data in list:
        number_name = str(data[0]).zfill(3)
        if number_name not in master_data:
            master_data[number_name] = {}
        if data[1]:
            edition_name = str(f"{data[1]}. Ausgabe")
            if edition_name not in master_data[number_name]:
                master_data[number_name][edition_name] = {
                    'name': data[3],
                    'editions': []
                }

            if data[2]:
                master_data[number_name][edition_name]['editions'].append(data[2])

    return master_data


@register.simple_tag()
def get_stock_number_data():
    data = {}

    all_number_query_exist = LTBNumberSet.objects.filter(editions__ltbs__quants__isnull=False)
    all_number_query_missing = LTBNumberSet.objects.filter(editions__ltbs__quants__isnull=True)

    for ltb_type in LTBType.objects.all():
        # Hoping that Django filters without DB access in the QuerySet
        number_query_exist = all_number_query_exist.filter(ltb_type=ltb_type)
        number_query_missing = all_number_query_missing.filter(ltb_type=ltb_type)

        data[ltb_type.code] = {
            'name': ltb_type.name,
            'code': ltb_type.code,
            'count_exists': len(number_query_exist),
            'count_all': get_all1_numbers(ltb_type),
            'missing_numbers': list(
                map(lambda number: str(number).zfill(3),
                    list(number_query_missing.values_list('ltb_number', flat=True)))),
        }
    return data
