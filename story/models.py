from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from person.models import Person
from .scraper import Story as s_Story, Person as s_Person, StoryScraper


class Genre(models.Model):
    name = models.CharField("Code", max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        return f"{self.name}"

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        return self.name

    def save(self, *args, **kwargs):
        """
        TODO: Docstring

        :param args:
        :param kwargs:
        :return:
        """
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)


class Story(models.Model):
    title = models.CharField("Title", max_length=255, null=True, blank=True)
    code = models.CharField("Code", max_length=255, unique=True)
    url = models.CharField("Book Url", max_length=255, null=True, blank=True)
    original_title = models.CharField("Original Title", max_length=255, null=True, blank=True)
    origin = models.CharField("Origin", max_length=255, null=True, blank=True)
    pages = models.PositiveIntegerField("Pages", null=True, blank=True)
    date = models.DateField("Release Date", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    author = models.ForeignKey(Person, related_name='stories_of_author', on_delete=models.RESTRICT, null=True, blank=True)
    illustrator = models.ForeignKey(Person, related_name='stories_of_illustrator', on_delete=models.RESTRICT, null=True,
                                    blank=True)
    characters = models.ManyToManyField(Person, related_name='stories_of_character', blank=True)
    genre = models.ManyToManyField(Genre, related_name='genre', blank=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['title']

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        return f"{self.code} - {self.title}"

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        return self.code

    def save(self, *args, **kwargs):
        """
        TODO: Docstring

        :param args:
        :param kwargs:
        :return:
        """
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)

    @staticmethod
    def get_or_create_artist(artist_data: s_Person, type: str):
        if artist_data.name:
            artist = Person.objects.filter(name=artist_data.name).first()
            if not artist:
                artist = Person(name=artist_data.name, url=artist_data.url, type=type)
                artist.save()
                artist.fetch_data()
            return artist
        else:
            return None

    @staticmethod
    def get_or_create_genre(genre_name: str):
        if genre_name:
            genre = Genre.objects.filter(name=genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
                genre.save()
            return genre
        else:
            return None

    def _fetch_characters(self, characters):
        self.characters.clear()
        char: Person
        for char in characters:
            c_data = self.get_or_create_artist(char, 'fictional')
            if c_data:
                self.characters.add(c_data)

    def _fetch_genres(self, genres):
        self.genre.clear()
        for genre in genres:
            g_data = self.get_or_create_genre(genre)
            if g_data:
                self.genre.add(g_data)

    def fetch_data(self):
        if self.url and self.code:
            data = StoryScraper(self.url).get_story_data()
            for s in data:
                if s.code == self.code:
                    self.title = s.title
                    self.original_title = s.original_title
                    self.date = s.date
                    self.origin = s.origin
                    self.pages = s.pages
                    self.author = self.get_or_create_artist(s.author, 'real')
                    self.illustrator = self.get_or_create_artist(s.illustrator, 'real')
                    self._fetch_characters(s.characters)
                    self._fetch_genres(s.genres)
                    self.save()

    def get_genres(self):
        return ", ".join([g.name for g in self.genre.all()])

    def get_absolute_url(self):
        """
        TODO: Docstring

        :return:
        """
        return reverse('story:story_detail',
                       args=[self.slug])