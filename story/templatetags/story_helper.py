from django import template
from ltb.models import LTBStory, LTB

register = template.Library()


@register.simple_tag()
def get_story_page(story, ltb):
    ltb_story = LTBStory.objects.filter(story=story, ltb=ltb).first()
    return ltb_story.page


@register.simple_tag()
def get_story_ltbs(story):
    return LTB.objects.filter(ltb_story_rel__story=story).values_list(
        "ltb_edition__ltb_number_set__ltb_type__code",
        "ltb_edition__ltb_number_set__ltb_number__number",
        "ltb_edition__title",
        "ltb_edition__ltb_edition_number__number",
        "name",
        "slug").distinct().all()
