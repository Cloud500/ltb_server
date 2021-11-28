from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from django.db import connection

from .scraper import LTBScraper


class LTBType(models.Model):
    name = models.CharField("Name", max_length=255)
    code = models.CharField("Code", max_length=10, unique=True)
    auto_url = models.BooleanField("Set number url")
    type_url = models.CharField("Type Url", max_length=255, default="/ausgaben/alle-ausgaben", null=True, blank=True)
    current_number = models.PositiveIntegerField("Current Number", null=True, blank=True)
    slug = models.SlugField(max_length=3, unique=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return str(self.code)

    def create_slug(self):
        return self

    def save(self, *args, **kwargs):
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)

    def first_number(self):
        return self.sets.first()

    def last_number(self):
        return self.sets.last()

    def all_numbers(self):
        return self.sets.all()

    def create_books(self):
        for number in range(1, self.current_number + 1):
            ltb_number = LTBNumber.objects.filter(number=number).first()
            if not ltb_number:
                ltb_number = LTBNumber(number=number)
                ltb_number.save()
            ltb_number_set = LTBNumberSet.objects.filter(ltb_number=ltb_number, ltb_type=self).first()
            if not ltb_number_set:
                ltb_number_set = LTBNumberSet(ltb_number=ltb_number, ltb_type=self)
                ltb_number_set.save()
            ltb_number_set.create_editions()


class LTBNumber(models.Model):
    number = models.PositiveIntegerField("Number", unique=True)
    slug = models.SlugField(max_length=3, unique=True)

    class Meta:
        ordering = ['number']

    def filled_number(self):
        return f"{str(self.number).zfill(3)}"

    def __str__(self):
        return self.filled_number()

    def create_slug(self):
        return self.filled_number()

    def save(self, *args, **kwargs):
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)

    def get_next_number(self):
        all_numbers = LTBNumber.objects.all()
        filtered_numbers = all_numbers.filter(number__gte=self.number)
        excluded_numbers = filtered_numbers.exclude(id=self.id)
        ordered_numbers = excluded_numbers.order_by('number')
        return ordered_numbers.first()

    def get_previous_number(self):
        all_numbers = LTBNumber.objects.all()
        filtered_numbers = all_numbers.filter(number__lte=self.number)
        excluded_numbers = filtered_numbers.exclude(id=self.id)
        ordered_numbers = excluded_numbers.order_by('-number')
        return ordered_numbers.first()


class LTBNumberSet(models.Model):
    ltb_number = models.ForeignKey(LTBNumber, related_name='sets', on_delete=models.CASCADE)
    ltb_type = models.ForeignKey(LTBType, related_name='sets', on_delete=models.CASCADE)
    url = models.CharField("Url", max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=3, unique=True)

    class Meta:
        ordering = ['ltb_number']
        unique_together = ('ltb_type', 'ltb_number',)

    def __str__(self):
        code = self.ltb_type.code
        number = self.ltb_number.filled_number()
        return f"{code}{number}"

    def create_slug(self):
        type_slug = self.ltb_type.slug
        number_slug = self.ltb_number.slug
        return f"{type_slug}{number_slug}"

    def save(self, *args, **kwargs):
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        if not self.url and self.ltb_type.auto_url:
            self.url = self.get_url()
        super().save(*args, **kwargs)

    def all_editions(self):
        return self.editions.all()

    def get_url(self):
        scraper = LTBScraper(self.ltb_number.number, self.ltb_type.type_url)
        return scraper.url

    def create_editions(self):
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
                special_edition = LTB(
                    ltb_edition=edition,
                    sort=1,
                    image_url=book_data['image_url']
                )
                special_edition.save()


class LTBEditionNumber(models.Model):
    number = models.PositiveIntegerField("Edition number", unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ['number', ]

    def __str__(self):
        return f"{self.number}. Auflage"

    def create_slug(self):
        return f"e{self.number}"

    def save(self, *args, **kwargs):
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)


class LTBEdition(models.Model):
    ltb_number_set = models.ForeignKey(LTBNumberSet, related_name='editions', on_delete=models.CASCADE)
    ltb_edition_number = models.ForeignKey(LTBEditionNumber, related_name='editions', on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=255)
    url = models.CharField("Url", max_length=255)
    stories = models.PositiveIntegerField("Stories", null=True, blank=True)
    pages = models.PositiveIntegerField("Pages", null=True, blank=True)
    release_date = models.DateField("Release Date", null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        unique_together = ('ltb_number_set', 'ltb_edition_number')
        ordering = ['ltb_number_set', 'ltb_edition_number']

    def __str__(self):
        type_string = self.ltb_number_set.ltb_type.code
        number_string = self.ltb_number_set.ltb_number.filled_number()
        title_string = self.title
        edition_string = f"{self.ltb_edition_number.number}. Auflage"
        return f"{type_string}{number_string} - {title_string} {edition_string}"

    def create_slug(self):
        number_slug = self.ltb_number_set.slug
        edition_number_slug = self.ltb_edition_number.slug
        return f"{number_slug}_{edition_number_slug}"

    def save(self, *args, **kwargs):
        if not self.id or self.slug != slugify(self.create_slug()):
            self.slug = slugify(self.create_slug())
        super().save(*args, **kwargs)


class InStockManager(models.Manager):
    def get_queryset(self):
        id_list = []
        query_set = super(InStockManager, self).get_queryset()
        for book in query_set:
            if book.inventory_count() > 0:
                id_list.append(book.id)

        query_set = query_set.filter(id__in=id_list)
        return query_set


class NotInStockManager(models.Manager):
    def get_queryset(self):
        id_list = []
        query_set = super(NotInStockManager, self).get_queryset()
        for book in query_set:
            if book.inventory_count() == 0:
                id_list.append(book.id)

        query_set = query_set.filter(id__in=id_list)
        return query_set


class LTB(models.Model):
    ltb_edition = models.ForeignKey(LTBEdition, related_name='ltbs', on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255, null=True, blank=True)
    complete_name = models.CharField("Complete Name", max_length=255, null=True, blank=True)
    sort = models.PositiveIntegerField("Sort")
    image_url = models.CharField("Image Url", max_length=255, null=True, blank=True)
    image = models.ImageField("Image", upload_to='cover/', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)

    objects = models.Manager()
    in_stock = InStockManager()
    not_in_stock = NotInStockManager()

    class Meta:
        unique_together = ('ltb_edition', 'sort')
        ordering = ['ltb_edition__ltb_number_set__ltb_type', 'ltb_edition__ltb_number_set__ltb_number',
                    'ltb_edition__ltb_edition_number', 'sort']

    @property
    def complete_name_calc(self):
        title_string = self.ltb_edition.title
        ltb_string = f" ({self.name})" if self.name else ""
        return f"{title_string}{ltb_string}"

    @property
    def edition(self):
        edition_string = f"{self.ltb_edition.ltb_edition_number.number}. Auflage"
        return edition_string

    @property
    def number(self):
        return self.ltb_edition.ltb_number_set.ltb_number.filled_number()

    @property
    def type(self):
        return self.ltb_edition.ltb_number_set.ltb_type.name

    @property
    def stories(self):
        return self.ltb_edition.stories

    @property
    def pages(self):
        return self.ltb_edition.pages

    @property
    def release_date(self):
        return self.ltb_edition.release_date

    def __str__(self):
        type_string = self.ltb_edition.ltb_number_set.ltb_type.code
        number_string = self.number
        name = self.complete_name
        edition_string = self.edition
        return f"{type_string}{number_string} - {name} {edition_string}"

    def create_slug(self):
        edition_slug = self.ltb_edition.slug
        return f"{edition_slug}_{self.sort}"

    def get_absolute_url(self):
        return reverse('ltb:book_detail',
                       args=[self.slug])

    def save(self, *args, **kwargs):
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
        ltb_number = self.ltb_edition.ltb_number_set.ltb_number.get_next_number()
        if ltb_number:
            ltb = LTB.objects.filter(
                ltb_edition__ltb_number_set__ltb_type=self.ltb_edition.ltb_number_set.ltb_type,
                ltb_edition__ltb_number_set__ltb_number=ltb_number,
                ltb_edition__ltb_edition_number__number=1).first()
            return ltb
        return None

    def previous_ltb(self):
        ltb_number = self.ltb_edition.ltb_number_set.ltb_number.get_previous_number()
        if ltb_number:
            ltb = LTB.objects.filter(
                ltb_edition__ltb_number_set__ltb_type=self.ltb_edition.ltb_number_set.ltb_type,
                ltb_edition__ltb_number_set__ltb_number=ltb_number,
                ltb_edition__ltb_edition_number__number=1).first()
            return ltb
        return None

    def all_ltb_editions(self):
        editions = LTB.objects.filter(ltb_edition__ltb_number_set=self.ltb_edition.ltb_number_set,
                                      sort=1).all()
        return editions

    def ltb_editions_count(self):
        editions = self.all_ltb_editions()
        if editions:
            return len(editions)
        return 0

    def all_ltb_versions(self):
        versions = LTB.objects.filter(ltb_edition=self.ltb_edition).all()
        return versions

    def ltb_versions_count(self):
        versions = self.all_ltb_versions()
        if versions:
            return len(versions)
        return 0

    def inventory_count(self):
        return len(self.quants.all())

    def have_first_edition(self):
        quant_count = len(self.quants.filter(is_first_edition=1))
        if quant_count > 0:
            return True
        return False
