from django import template
from stock.models import Quant

register = template.Library()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    TODO: Docstring

    :param context:
    :param kwargs:
    :return:
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


@register.simple_tag()
def addition(num1: int, num2: int) -> int:
    """
    Addition of two numbers

    :param num1: first number
    :type num1: int
    :param num2: second number
    :type num2: int
    :return: addition of the numbers
    :rtype: int
    """
    return num1 + num2


@register.simple_tag()
def last_stock_number(type_code: str) -> str:
    """
    Get the highest number in stock.

    :param type_code: code of the ltb type
    :type type_code: str
    :return: highest number as string "XXX"
    :rtype str
    """
    last_quant = Quant.objects.filter(book__ltb_edition__ltb_number_set__ltb_type__code=type_code).order_by(
        "book__ltb_edition__ltb_number_set__ltb_number__number").last()
    if last_quant:
        return last_quant.book.number
    else:
        return "000"


@register.simple_tag()
def compare_string_number(number1: str, number2: str) -> bool:
    """
    Compare 2 strings (die Zahlen sind) and return True if the first is smaller than the second.

    :param number1: "smaller" number to compare
    :type number1: str
    :param number2: "bigger" number to compare
    :type number2: str
    :return: compare result
    :rtype: bool
    """
    if int(number1) < int(number2):
        return True
    return False
