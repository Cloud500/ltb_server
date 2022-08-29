from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from .scraper import get_image
from .scraper import PersonScraper

# from ltb.models import LTBStory


class Person(models.Model):
    TYPES = [
        ("real", "Real person"),
        ("fictional", "Fictional Person"),
    ]

    name = models.CharField("Name", max_length=255, unique=True)
    url = models.CharField("Person Url", max_length=255, null=True, blank=True)
    description = models.TextField("Description", null=True, blank=True)
    image_url = models.CharField("Image Url", max_length=255, null=True, blank=True)
    image = models.ImageField("Image", upload_to='person/', null=True, blank=True)
    type = models.CharField("Type", max_length=255, choices=TYPES)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Person'
        verbose_name_plural = 'Personen'
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

        if not self.image and self.image_url:
            name, image = get_image(self.image_url)
            self.image.save(name, image)

        super().save(*args, **kwargs)

    def fetch_data(self):
        if self.url:
            data = PersonScraper(self.url).get_artist_data()
            self.name = data.name
            self.description = data.description
            self.image_url = data.url
            self.save()

    def get_real_absolute_url(self):
        """
        TODO: Docstring

        :return:
        """
        return reverse('person:real_person_detail',
                       args=[self.slug])

    def get_fictional_absolute_url(self):
        """
        TODO: Docstring

        :return:
        """
        return reverse('person:fictional_person_detail',
                       args=[self.slug])

    # def get_character_stories(self):
    #     # ltbs = LTB.objects.filter(ltb_edition__LTBEditionStory__story__characters__in=self).all()
    #     stories = self.stories_of_character.all()
    #     # test = stories.LTBEditionStory.all()
    #     return stories
    #
    # # def get_character_ltbs(self):
    # #     ltbs = LTB.objects.filter(ltb_story_rel__story__characters=self).distinct()
    # #     # test2 = LTBStory.objects.filter(story__in=self.get_character_stories()).distinct()
    # #     return ltbs
