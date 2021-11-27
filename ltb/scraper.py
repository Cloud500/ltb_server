import os
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

from django.core.files.temp import NamedTemporaryFile
from django.core.files import File


class LTBScraper:
    def __init__(self, number: int, type_url: str = None):
        if not type_url:
            type_url = "/ausgaben/alle-ausgaben"

        self._number = number
        self._base_url = "https://www.lustiges-taschenbuch.de"
        self._type_url = type_url

    @property
    def filter(self):
        return f"?issue[min]={self._number}&issue[max]={self._number}"

    @property
    def url(self):
        return f"{self._base_url}{self._type_url}{self.filter}"

    def get_edition_urls(self):
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
    def _get_sidebar(html):
        return html.find(id="page-sidebar")

    @staticmethod
    def _get_editions(html):
        return html.find(class_="issue-editions")

    @staticmethod
    def _get_title(html):
        return html.find("span", class_="field--name-title").text

    def _get_story_count(self, html):
        sidebar = self._get_sidebar(html)
        return int(sidebar.find("dt", text="Anzahl Geschichten").findNext("dd").string)

    def _get_page_count(self, html):
        sidebar = self._get_sidebar(html)
        try:
            return int(sidebar.find("dt", text="Comicseiten").findNext("dd").string)
        except AttributeError:
            return 0

    def _get_release_date(self, html):
        sidebar = self._get_sidebar(html)
        date = sidebar.find("dt", text="Erscheinungs­datum").findNext("dd").string
        return datetime.strptime(date, "%d.%m.%Y")

    def _get_edition(self, html):
        editions = self._get_editions(html)
        if editions:
            edition = editions.find("a", class_="active").string
            return int(str(edition).split(".")[0])
        else:
            return 1

    def get_data(self, url):
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
    def get_image(image_url):
        name = os.path.basename(image_url)
        img_tmp = NamedTemporaryFile()
        with urlopen(image_url) as uo:
            assert uo.status == 200
            img_tmp.write(uo.read())
            img_tmp.flush()
        image = File(img_tmp)
        return name, image

    def get_edition_data(self, urls_data):
        for url_data in urls_data:
            url_data.update(self.get_data(url_data['url']))
        return list(urls_data)
