from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.db import connection

from story.scraper import StoryScraper, Story as s_Story
from .scraper import LTBScraper

from story.models import Story


class LTBType(models.Model):
    """
    TODO: Docstring
    """
    name = models.CharField("Name", max_length=255)
    code = models.CharField("Code", max_length=10, unique=True)
    auto_url = models.BooleanField("Set number url")
    type_url = models.CharField("Type Url", max_length=255, default="/ausgaben/alle-ausgaben", null=True, blank=True)
    current_number = models.PositiveIntegerField("Current Number", null=True, blank=True)
    auto_fetch = models.BooleanField("Auto fetch books")
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Typ'
        verbose_name_plural = 'Typen'
        ordering = ['code']
        permissions = [
            ('fetch_new_books', "Can fetch new books"),
        ]

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        return str(self.code)

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        return self

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

    def first_number(self):
        """
        TODO: Docstring

        :return:
        """
        return self.sets.first()

    def last_number(self):
        """
        TODO: Docstring

        :return:
        """
        return self.sets.last()

    def all_numbers(self):
        """
        TODO: Docstring

        :return:
        """
        return self.sets.all()

    @staticmethod
    def get_or_create_number(number: int):
        """
        TODO: Docstring

        :param number:
        :return:
        """
        ltb_number = LTBNumber.objects.filter(number=number).first()
        if not ltb_number:
            ltb_number = LTBNumber(number=number)
            ltb_number.save()
        return ltb_number

    def get_or_create_number_set(self, ltb_number):
        """
        TODO: Docstring

        :param ltb_number:
        :return:
        """
        ltb_number_set = LTBNumberSet.objects.filter(ltb_number=ltb_number, ltb_type=self).first()
        if not ltb_number_set:
            ltb_number_set = LTBNumberSet(ltb_number=ltb_number, ltb_type=self)
            ltb_number_set.save()
        return ltb_number_set

    def create_books(self):
        """
        TODO: Docstring

        :return:
        """
        for number in range(1, self.current_number + 1):
            ltb_number = self.get_or_create_number(number)
            ltb_number_set = self.get_or_create_number_set(ltb_number)
            ltb_number_set.create_editions()

    def fetch_next_number(self):
        """
        TODO: Docstring

        :return:
        """
        if self.auto_fetch:
            number = self.current_number + 1
            type_url = self.type_url
            scraper = LTBScraper(number, type_url)
            urls = scraper.get_edition_urls()
            if urls:
                self.current_number = number
                self.save()
                for _ in urls:
                    ltb_number = self.get_or_create_number(number)
                    ltb_number_set = self.get_or_create_number_set(ltb_number)
                    ltb_number_set.create_editions()


class LTBNumber(models.Model):
    """
    TODO: Docstring
    """
    number = models.PositiveIntegerField("Number", unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Nummer'
        verbose_name_plural = 'Nummern'
        ordering = ['number']

    def filled_number(self):
        """
        TODO: Docstring

        :return:
        """
        return f"{str(self.number).zfill(3)}"

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        return self.filled_number()

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        return self.filled_number()

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

    def get_next_number(self):
        """
        TODO: Docstring

        :return:
        """
        all_numbers = LTBNumber.objects.all()
        filtered_numbers = all_numbers.filter(number__gte=self.number)
        excluded_numbers = filtered_numbers.exclude(id=self.id)
        ordered_numbers = excluded_numbers.order_by('number')
        return ordered_numbers.first()

    def get_previous_number(self):
        """
        TODO: Docstring

        :return:
        """
        all_numbers = LTBNumber.objects.all()
        filtered_numbers = all_numbers.filter(number__lte=self.number)
        excluded_numbers = filtered_numbers.exclude(id=self.id)
        ordered_numbers = excluded_numbers.order_by('-number')
        return ordered_numbers.first()


class LTBNumberSet(models.Model):
    """
    TODO: Docstring
    """
    ltb_number = models.ForeignKey(LTBNumber, related_name='sets', on_delete=models.CASCADE)
    ltb_type = models.ForeignKey(LTBType, related_name='sets', on_delete=models.CASCADE)
    url = models.CharField("Url", max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Nummer set'
        verbose_name_plural = 'Nummer sets'
        ordering = ['ltb_number']
        unique_together = ('ltb_type', 'ltb_number',)

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        code = self.ltb_type.code
        number = self.ltb_number.filled_number()
        return f"{code}{number}"

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        type_slug = self.ltb_type.slug
        number_slug = self.ltb_number.slug
        return f"{type_slug}{number_slug}"

    def save(self, *args, **kwargs):
        """
        TODO: Docstring

        :param args:
        :param kwargs:
        :return:
        """
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        if not self.url and self.ltb_type.auto_url:
            self.url = self.get_url()
        super().save(*args, **kwargs)

    def all_editions(self):
        """
        TODO: Docstring

        :return:
        """
        return self.editions.all()

    def get_url(self):
        """
        TODO: Docstring

        :return:
        """
        scraper = LTBScraper(self.ltb_number.number, self.ltb_type.type_url)
        return scraper.url

    def create_editions(self):
        """
        TODO: Docstring

        :return:
        """
        scraper = LTBScraper(self.ltb_number.number, self.ltb_type.type_url)
        urls = scraper.get_edition_urls()
        data = scraper.get_edition_data(urls)

        for book_data in data:
            ltb_edition_number = LTBEditionNumber.objects.filter(number=book_data['edition']).first()
            if not ltb_edition_number:
                ltb_edition_number = LTBEditionNumber(number=book_data['edition'])
                ltb_edition_number.save()

            edition = self.all_editions().filter(ltb_edition_number=ltb_edition_number).first()

            if not edition:
                edition = LTBEdition(
                    ltb_number_set=self,
                    ltb_edition_number=ltb_edition_number,
                    url=book_data['url'],
                    title=book_data['title'],
                    stories=book_data['story_count'],
                    pages=book_data['page_count'],
                    release_date=book_data['release_date']
                )
                edition.save()
                edition.fetch_stories()
                special_edition = LTB(
                    ltb_edition=edition,
                    sort=1,
                    is_read=0,
                    image_url=book_data['image_url']
                )
                special_edition.save()


class LTBEditionNumber(models.Model):
    """
    TODO: Docstring
    """
    number = models.PositiveIntegerField("Edition number", unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Auflage'
        verbose_name_plural = 'Auflagen'
        ordering = ['number', ]

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        return f"{self.number}. Auflage"

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        return f"e{self.number}"

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


class LTBEdition(models.Model):
    """
    TODO: Docstring
    """
    ltb_number_set = models.ForeignKey(LTBNumberSet, related_name='editions', on_delete=models.CASCADE)
    ltb_edition_number = models.ForeignKey(LTBEditionNumber, related_name='editions', on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=255)
    url = models.CharField("Url", max_length=255)
    stories = models.PositiveIntegerField("Stories", null=True, blank=True)
    pages = models.PositiveIntegerField("Pages", null=True, blank=True)
    release_date = models.DateField("Release Date", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Buchversion'
        verbose_name_plural = 'Buchversionen'
        unique_together = ('ltb_number_set', 'ltb_edition_number')
        ordering = ['ltb_number_set', 'ltb_edition_number']

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        type_string = self.ltb_number_set.ltb_type.code
        number_string = self.ltb_number_set.ltb_number.filled_number()
        title_string = self.title
        edition_string = f"{self.ltb_edition_number.number}. Auflage"
        return f"{type_string}{number_string} - {title_string} {edition_string}"

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        number_slug = self.ltb_number_set.slug
        edition_number_slug = self.ltb_edition_number.slug
        return f"{number_slug}_{edition_number_slug}"

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

    # def get_or_create_story(self, story_data: s_Story):
    #     edition_story = self.LTBEditionStory.filter(story__code=story_data.code).first()
    #     # edition_story = LTBEditionStory.objects.filter(ltb_edition__id=self.id, story__code=story_data.code).first()
    #
    #     if not edition_story:
    #         story = Story.objects.filter(code=story_data.code).first()
    #
    #         if not story:
    #             story = Story(code=story_data.code, url=self.url)
    #             story.save()
    #             story.fetch_data()
    #
    #         edition_story = LTBEditionStory(ltb_edition=self, story=story, page=story_data.page)
    #         edition_story.save()
    #     return edition_story
    #
    # def fetch_stories(self):
    #     if self.url:
    #         data = StoryScraper(self.url).get_story_data()
    #         story: s_Story
    #         for story in data:
    #             self.get_or_create_story(story)


# class LTBEditionStory(models.Model):
#     ltb_edition = models.ForeignKey(LTBEdition, related_name='LTBEditionStory', on_delete=models.CASCADE)
#     story = models.ForeignKey(Story, related_name='LTBEditionStory', on_delete=models.CASCADE)
#     page = models.PositiveIntegerField("Stories", null=True, blank=True)
#
#     class Meta:
#         """
#         TODO: Docstring
#         """
#         verbose_name = 'Book, Story real'
#         verbose_name_plural = 'Books, Story real'
#         unique_together = ('ltb_edition', 'story')
#         ordering = ['page']


class InStockManager(models.Manager):
    """
    TODO: Docstring
    """

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        id_list = []
        query_set = super(InStockManager, self).get_queryset()
        for book in query_set:
            if book.inventory_count() > 0:
                id_list.append(book.id)

        query_set = query_set.filter(id__in=id_list)
        return query_set


class NotInStockManager(models.Manager):
    """
    TODO: Docstring
    """

    def get_queryset(self):
        """
        TODO: Docstring

        :return:
        """
        id_list = []
        query_set = super(NotInStockManager, self).get_queryset()
        for book in query_set:
            if book.inventory_count() == 0:
                id_list.append(book.id)

        query_set = query_set.filter(id__in=id_list)
        return query_set


class LTB(models.Model):
    """
    TODO: Docstring
    """
    ltb_edition = models.ForeignKey(LTBEdition, related_name='ltbs', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255, null=True, blank=True)
    complete_name = models.CharField("Complete Name", max_length=255, null=True, blank=True)
    sort = models.PositiveIntegerField("Sort")
    image_url = models.CharField("Image Url", max_length=255, null=True, blank=True)
    image = models.ImageField("Image", upload_to='cover/', null=True, blank=True)
    is_read = models.BooleanField("Gelesen")
    slug = models.SlugField(max_length=255, unique=True)

    objects = models.Manager()
    in_stock = InStockManager()
    not_in_stock = NotInStockManager()

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Buch'
        verbose_name_plural = 'Bücher'
        unique_together = ('ltb_edition', 'sort')
        ordering = ['ltb_edition__ltb_number_set__ltb_type', 'ltb_edition__ltb_number_set__ltb_number',
                    'ltb_edition__ltb_edition_number', 'sort']

    @property
    def complete_name_calc(self):
        """
        TODO: Docstring

        :return:
        """
        title_string = self.ltb_edition.title
        ltb_string = f" ({self.name})" if self.name else ""
        return f"{title_string}{ltb_string}"

    @property
    def edition(self):
        """
        TODO: Docstring

        :return:
        """
        edition_string = f"{self.ltb_edition.ltb_edition_number.number}. Auflage"
        return edition_string

    @property
    def edition_id(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_edition_number.id

    @property
    def type_code(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_number_set.ltb_type.code

    @property
    def number(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_number_set.ltb_number.filled_number()

    @property
    def number_id(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_number_set.ltb_number.id

    @property
    def type(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_number_set.ltb_type.name

    @property
    def type_id(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.ltb_number_set.ltb_type.id

    @property
    def stories(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.stories

    @property
    def pages(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.pages

    @property
    def release_date(self):
        """
        TODO: Docstring

        :return:
        """
        return self.ltb_edition.release_date

    def __str__(self):
        """
        TODO: Docstring

        :return:
        """
        type_string = self.ltb_edition.ltb_number_set.ltb_type.code
        number_string = self.number
        name = self.complete_name
        version_string = self.name
        edition_string = self.edition

        complete_name = f"{type_string}{number_string} - {name}"

        if version_string:
            complete_name = f"{complete_name} - {version_string}"

        if self.ltb_editions_count() > 1:
            complete_name = f"{complete_name} ({edition_string})"

        return complete_name

    def create_slug(self):
        """
        TODO: Docstring

        :return:
        """
        edition_slug = self.ltb_edition.slug
        return f"{edition_slug}_{self.sort}"

    def get_absolute_url(self):
        """
        TODO: Docstring

        :return:
        """
        return reverse('ltb:book_detail',
                       args=[self.slug])

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
            scraper = LTBScraper(self.ltb_edition.ltb_number_set.ltb_number.number,
                                 self.ltb_edition.ltb_number_set.ltb_type.type_url)
            name, image = scraper.get_image(self.image_url)
            self.image.save(name, image)
        if not self.complete_name or self.complete_name != self.complete_name_calc:
            self.complete_name = self.complete_name_calc
        super().save(*args, **kwargs)

    def next_ltb(self):
        """
        TODO: Docstring

        :return:
        """
        ltb_number = self.ltb_edition.ltb_number_set.ltb_number.get_next_number()
        if ltb_number:
            ltb = LTB.objects.filter(
                ltb_edition__ltb_number_set__ltb_type=self.ltb_edition.ltb_number_set.ltb_type,
                ltb_edition__ltb_number_set__ltb_number=ltb_number,
                ltb_edition__ltb_edition_number__number=1).first()
            return ltb
        return None

    def previous_ltb(self):
        """
        TODO: Docstring

        :return:
        """
        ltb_number = self.ltb_edition.ltb_number_set.ltb_number.get_previous_number()
        if ltb_number:
            ltb = LTB.objects.filter(
                ltb_edition__ltb_number_set__ltb_type=self.ltb_edition.ltb_number_set.ltb_type,
                ltb_edition__ltb_number_set__ltb_number=ltb_number,
                ltb_edition__ltb_edition_number__number=1).first()
            return ltb
        return None

    def all_ltb_editions(self):
        """
        TODO: Docstring

        :return:
        """
        editions = LTB.objects.filter(ltb_edition__ltb_number_set=self.ltb_edition.ltb_number_set,
                                      sort=1).all()
        return editions

    def ltb_editions_count(self):
        """
        TODO: Docstring

        :return:
        """
        editions = self.all_ltb_editions()
        if editions:
            return len(editions)
        return 0

    def all_ltb_versions(self):
        """
        TODO: Docstring

        :return:
        """
        versions = LTB.objects.filter(ltb_edition=self.ltb_edition).all()
        return versions

    def ltb_versions_count(self):
        """
        TODO: Docstring

        :return:
        """
        versions = self.all_ltb_versions()
        if versions:
            return len(versions)
        return 0

    def inventory_count(self):
        """
        TODO: Docstring

        :return:
        """
        return len(self.quants.all())

    def have_first_edition(self):
        """
        TODO: Docstring

        :return:
        """
        quant_count = len(self.quants.filter(is_first_edition=1))
        if quant_count > 0:
            return True
        return False

    def get_or_create_story(self, story_data: s_Story):
        edition_story = self.ltb_story_rel.filter(story__code=story_data.code).first()

        if not edition_story:
            story = Story.objects.filter(code=story_data.code).first()

            if not story:
                story = Story(code=story_data.code, url=self.ltb_edition.url)
                story.save()
                story.fetch_data()

            edition_story = LTBStory(ltb=self, story=story, page=story_data.page)
            edition_story.save()
        return edition_story

    def fetch_stories(self):
        if self.ltb_edition.url:
            data = StoryScraper(self.ltb_edition.url).get_story_data()
            story: s_Story
            for story in data:
                self.get_or_create_story(story)

    def get_stories(self):
        stories = Story.objects.filter(ltb_story_rel__ltb=self).order_by('ltb_story_rel__pages').all()
        return stories


class LTBStory(models.Model):
    ltb = models.ForeignKey('LTB', related_name='ltb_story_rel', on_delete=models.CASCADE)
    story = models.ForeignKey("story.Story", related_name='ltb_story_rel', on_delete=models.CASCADE)
    page = models.PositiveIntegerField("Stories", null=True, blank=True)

    class Meta:
        """
        TODO: Docstring
        """
        verbose_name = 'Book, Story real'
        verbose_name_plural = 'Books, Story real'
        unique_together = ('ltb', 'story')
        ordering = ['page']
