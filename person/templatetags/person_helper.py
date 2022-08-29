from django import template
from ltb.models import LTB
from story.models import Story

register = template.Library()


@register.simple_tag()
def get_character_stories(character):
    return Story.objects.filter(characters=character).values_list("title", "code", "slug").all()


@register.simple_tag()
def get_author_stories(person):
    return Story.objects.filter(author=person).values_list("title", "code", "slug").all()


@register.simple_tag()
def get_illustrator_stories(person):
    return Story.objects.filter(illustrator=person).values_list("title", "code", "slug").all()


@register.simple_tag()
def get_character_ltbs(character):
    return LTB.objects.filter(ltb_story_rel__story__characters=character).values_list(
        "ltb_edition__ltb_number_set__ltb_type__code",
        "ltb_edition__ltb_number_set__ltb_number__number",
        "ltb_edition__title",
        "ltb_edition__ltb_edition_number__number",
        "name",
        "slug").distinct().all()
