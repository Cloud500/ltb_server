import os
import requests

from typing import Tuple

from bs4 import BeautifulSoup
from urllib.request import urlopen

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

BASE_URL = "https://www.lustiges-taschenbuch.de"


def get_image(image_url: str) -> Tuple[str, File]:
    """
    Download the image of the given image url

    :param image_url: Url of image
    :type image_url: str
    :return: Name and File of the Image
    :rtype: Tuple[str, File]
    """
    name = os.path.basename(image_url)
    img_tmp = NamedTemporaryFile()
    with urlopen(image_url) as uo:
        assert uo.status == 200
        img_tmp.write(uo.read())
        img_tmp.flush()
    image = File(img_tmp)
    return name, image


class Person:
    def __init__(self, name: str, description: str, url: str):
        self._name = name
        self._description = description
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def url(self) -> str:
        if self._url:
            return BASE_URL + self._url
        else:
            return ""

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)


class PersonScraper:

    def __init__(self, artist_url):
        self._artist_url = artist_url

    @staticmethod
    def _clean_text(text):
        if text:
            return text.replace("\n", "").strip()
        else:
            return None

    def _get_name(self, html):
        page_content = html.find("div", class_="showcase-about")
        name = None
        if page_content.find("h1") and page_content.find("h1").find("span"):
            name = self._clean_text(page_content.find("h1").find("span").string)
        return name

    def _get_description(self, html, name):
        page_content = html.find("div", class_="showcase-about")
        description = None
        if page_content.find("p"):
            description = self._clean_text(page_content.find("p").string)
        else:
            description = self._clean_text(page_content.text)
        if description == name:
            description = ""
        return description

    def _get_image_url(self, html):
        page_content = html.find("div", class_="showcase-subject")
        image_url = None
        if page_content.find("img"):
            image_url = page_content.find("img")['src']
        return image_url

    def get_artist_data(self) -> Person:
        page = requests.get(self._artist_url)
        html = BeautifulSoup(page.content, 'html.parser')
        name = self._get_name(html)
        description = self._get_description(html, name)
        image_url = self._get_image_url(html)
        return Person(name, description, image_url)
