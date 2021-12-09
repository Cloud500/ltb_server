from django import template
from .news_scraper import NewsScraper

register = template.Library()


@register.simple_tag()
def get_news() -> list:
    """
    Fetch News from lustiges-taschenbuch.de

    :return: list of news
    :rtype: list
    """
    return NewsScraper().news
