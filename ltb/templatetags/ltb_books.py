from django import template

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
