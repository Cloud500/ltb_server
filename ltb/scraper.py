import os
from typing import Tuple

import requests

from datetime import datetime
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.request import urlopen

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


class LTBScraper:
    """
    Fetch LTB Books from lustiges-taschenbuch.de
    """
    def __init__(self, number: int, type_url: str = None):
        """
        Fetch LTB Books from lustiges-taschenbuch.de

        :param number: number of the Book to fetch
        :type number: int
        :param type_url: type suburl of the Book to fetch
        :type type_url: str
        """
        if not type_url:
            type_url = "/ausgaben/alle-ausgaben"

        self._number = number
        self._base_url = "https://www.lustiges-taschenbuch.de"
        self._type_url = type_url

    @property
    def filter(self) -> str:
        """
        Give the filter string of the url

        :return: Url filter string
        :rtype: str
        """
        return f"?issue[min]={self._number}&issue[max]={self._number}"

    @property
    def url(self) -> str:
        """
        Give the complete url for the number/type combination.

        :return: complete url
        :rtype: str
        """
        return f"{self._base_url}{self._type_url}{self.filter}"

    def get_edition_urls(self) -> list:
        """
        Create a list of direct url and img url for each edition of the number/type combination.

        :return: list of edition uls
        :rtype: list
        """
        page = requests.get(self.url)
        html = BeautifulSoup(page.content, 'html.parser')
        page_content = html.find(id="page-content")
        books = page_content.find_all(class_="cemetery-tombstone")

        edition_urls = []
        for book in books:
            link = book.find("a")['href']
            image = book.find("img")['src']
            edition_urls.append({'url': self._base_url + link,
                                 'image_url': self._base_url + image})
        return edition_urls

    @staticmethod
    def _get_sidebar(html: Tag) -> Tag:
        """
        Get the page-sidebar content from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: page-sidebar content as bs4 Tag
        :rtype: Tag
        """
        return html.find(id="page-sidebar")

    @staticmethod
    def _get_editions(html: Tag) -> Tag:
        """
        Get the issue-editions content from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: issue-editions content as bs4 Tag
        :rtype: Tag
        """
        return html.find(class_="issue-editions")

    @staticmethod
    def _get_title(html: Tag) -> str:
        """
        Get the title from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: Title
        :rtype: str
        """
        return html.find("span", class_="field--name-title").text

    def _get_story_count(self, html: Tag) -> int:
        """
        Get the story count from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: Story count
        :rtype: int
        """
        sidebar = self._get_sidebar(html)
        try:
            return int(sidebar.find("dt", text="Anzahl Geschichten").findNext("dd").string)
        except AttributeError:
            return 0

    def _get_page_count(self, html: Tag) -> int:
        """
        Get the page count from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: Page count
        :rtype: int
        """
        sidebar = self._get_sidebar(html)
        try:
            return int(sidebar.find("dt", text="Comicseiten").findNext("dd").string)
        except AttributeError:
            return 0

    def _get_release_date(self, html: Tag) -> datetime:
        """
        Get the release date from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: Release date
        :rtype: datetime
        """
        sidebar = self._get_sidebar(html)
        date = sidebar.find("dt", text="Erscheinungs­datum").findNext("dd").string
        return datetime.strptime(date, "%d.%m.%Y")

    def _get_edition(self, html: Tag) -> int:
        """
        Get the edition number from the given bs4 Tag

        :param html: bs4 Tag
        :type html: Tag
        :return: Edition number
        :rtype: int
        """
        editions = self._get_editions(html)
        if editions:
            edition = editions.find("a", class_="active").string
            return int(str(edition).split(".")[0])
        else:
            return 1

    def get_data(self, url: str) -> dict:
        """
        Fetch all data from a given edition url.

        :param url: Url of the edition
        :type url: str
        :return: dict containing all data for the edition
        :rtype: dict
        """
        page = requests.get(url)
        html = BeautifulSoup(page.content, 'html.parser')
        title = self._get_title(html)
        story_count = self._get_story_count(html)
        page_count = self._get_page_count(html)
        release_date = self._get_release_date(html)
        edition = self._get_edition(html)
        return {
            'title': title,
            'story_count': story_count,
            'page_count': page_count,
            'release_date': release_date,
            'edition': edition
        }

    @staticmethod
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

    def get_edition_data(self, urls_data: list) -> list:
        """
        Add the ltb data to the urls_data list

        :param urls_data: list of ediiotn urls
        :type urls_data: list
        :return: complete list for all editions data
        :rtype: list
        """
        for url_data in urls_data:
            url_data.update(self.get_data(url_data['url']))
        return list(urls_data)
