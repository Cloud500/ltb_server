from django import template
from ..models import LTBType

register = template.Library()


@register.inclusion_tag('ltb/../../templates/navi_types.html')
def show_all_types(path):
    all_types = LTBType.objects.all()
    return {'all_types': all_types,
            'path': path}
