import requests
import teaser as teaser
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime


class NewsScraper:
    """
    Fetch news data from lustiges-taschenbuch.de

    """

    class News:
        """
        Storage of the news data.

        """

        def __init__(self, title: str, date: datetime, link: str):
            """
            Storage of the news data.

            Contains title, date and the link to the news

            :param title: Title of the news.
            :type title: str
            :param date: Date of the news.
            :type date: datetime
            :param link: Link to the news.
            :type link: str
            """
            self._title = title
            self._date = date
            self._link = link

        @property
        def title(self) -> str:
            """
            Get the title of the news.

            :return: Title of the news.
            :rtype: str
            """
            return self._title

        @property
        def date(self) -> str:
            """
            Get the date of the news as string.

            :return: Date of the news.
            :rtype: str
            """
            return self._date.strftime("%d.%m.%Y")

        @property
        def link(self) -> str:
            """
            Get the link of the news.

            :return: Link to the news.
            :rtype: str
            """
            return self._link

        def __str__(self) -> str:
            """
            Return str(self).

            :return: str(self)
            :rtype: str
            """
            return f"{self.date} - \"{self.title}\""

    def __init__(self):
        """
        Fetch news data from lustiges-taschenbuch.de

        Get the news and save them in the news list.
        """
        self._url = "https://www.lustiges-taschenbuch.de/news"
        self._news = []
        self.get_news()

    @property
    def news(self) -> list:
        """
        Get the news list.

        :return: List of news.
        :rtype: list
        """
        return self._news

    @staticmethod
    def _get_date(news: Tag) -> datetime:
        """
        Get the date from the bs4 Tag and convert it to a datetime.

        :param news: bs4 Tag
        :type news: Tag
        :return: Date of the news.
        :rtype: datetime
        """
        date_str = news.find(class_="block-title").text
        date_str = date_str.replace("News vom ", "")
        date = datetime.strptime(date_str, "%d.%m.%Y")
        return date

    @staticmethod
    def _get_title(news: Tag) -> str:
        """
        Get the title from the bs4 Tag and format it.

        :param news: bs4 Tag
        :type news: Tag
        :return: Title of the news.
        :rtype: str
        """
        title_raw = news.find(class_="note-title").text
        title = title_raw.replace("  ", "").replace("\n", "")
        return title

    @staticmethod
    def _get_link(news: Tag) -> str:
        """
        Get the link from the bs4 Tag and format it.

        :param news: bs4 Tag
        :type news: Tag
        :return: Link of the news.
        :rtype: str
        """
        link_raw = news.find(class_="teaser-link").findNext("a")['href']
        link = f"https://www.lustiges-taschenbuch.de{link_raw}"
        return link

    def get_news(self):
        """
        Gets the web page content, format it and create the news list.

        :return: None
        """
        page = requests.get(self._url)
        html = BeautifulSoup(page.content, 'html.parser')
        page_content = html.find("div", id="page-playground")
        news_list = page_content.find_all("div", class_="block")

        for news in news_list:
            date = self._get_date(news)
            title = self._get_title(news)
            link = self._get_link(news)
            self._news.append(self.News(title, date, link))
