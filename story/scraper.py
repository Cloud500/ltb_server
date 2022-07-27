from datetime import datetime

import requests

from bs4 import BeautifulSoup

BASE_URL = "https://www.lustiges-taschenbuch.de"


class Person:
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return BASE_URL + self._url

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return str(self.name)


class Story:
    def __init__(self):
        self.title = ""
        self.author = Person
        self.illustrator = Person
        self.genres = []
        self.characters = []
        self._code = None
        self.original_title = ""
        self.origin = ""
        self.date = None
        self.pages = 0
        self.page = 0

    @property
    def code(self) -> str:
        if self._code:
            return self._code
        elif self.date:
            return str(self.date)
        else:
            return self.title

    @code.setter
    def code(self, value: str):
        self._code = value

    def __str__(self) -> str:
        return str(self.title)

    def __repr__(self) -> str:
        return str(self.title)


class StoryScraper:
    def __init__(self, book_url):
        self._book_url = book_url

    @staticmethod
    def _clean_text(text, replace):
        return text.replace(replace, "").replace("\n", "").strip()

    def _get_title(self, row_header):
        title = ""
        if row_header.find("i"):
            title = self._clean_text(row_header.find("i").string, "")
        return str(title)

    def _get_person_data(self, row_header, person_type):
        name = ""
        url = ""
        if row_header.find("span", itemprop=person_type):
            person_data = row_header.find("span", itemprop=person_type)
            name = self._clean_text(person_data.find("span", itemprop="name").string, "")
            url = person_data.find("a")['href']
        return Person(str(name), url)

    @staticmethod
    def _get_characters(content):
        characters = []
        for character in content.find_all("a"):
            characters.append(
                Person(str(character.string), character["href"])
            )
        return characters

    @staticmethod
    def _get_genres(content):
        genres = []
        for genre in content.find_all("a"):
            genres.append(str(genre.string))
        return genres

    def _phrase_content(self, row_content, story: Story):
        story_content = row_content.find_all("small")
        for content in story_content:
            text = str(content.text)

            if text.find("Genre") > 0:
                story.genres = self._get_genres(content)
            elif text.find("Code") > 0:
                story.code = self._clean_text(text, "Code:")
            elif text.find("Originaltitel") > 0:
                story.original_title = self._clean_text(text, "Originaltitel:")
            elif text.find("Ursprung") > 0:
                story.origin = self._clean_text(text, "Ursprung:")
            elif text.find("Seitenanzahl") > 0:
                story.pages = int(self._clean_text(text, "Seitenanzahl:"))
            elif text.find("Charaktere") > 0:
                story.characters = self._get_characters(content)
            elif text.find("Erstveröffentlichung") > 0:
                story.date = datetime.strptime(content.find("time")["datetime"], '%Y-%m-%dT%H:%M:%SZ')

    @staticmethod
    def _get_story_page(row):
        content = row.find("td", class_="toc-pagenumber").text
        return int(content.replace("\n", "").strip())

    def _collect_story_data(self, row):
        row_header = row.find("div", class_="accordion-header")
        row_content = row.find("div", class_="accordion-content")
        story = Story()

        story.title = self._get_title(row_header)
        story.author = self._get_person_data(row_header, "author")
        story.illustrator = self._get_person_data(row_header, "contributor")
        self._phrase_content(row_content, story)
        story.page = self._get_story_page(row)
        return story

    def get_story_data(self) -> list[Story]:
        page = requests.get(self._book_url)
        html = BeautifulSoup(page.content, 'html.parser')
        table_body = html.find("table", class_="toc")
        rows = table_body.find_all('tr', {"class": "toc-chapter"})
        stories = []

        for row in rows:
            stories.append(self._collect_story_data(row))
        return stories
