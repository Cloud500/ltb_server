from django.db import models

from ltb.models import LTB


class Quant(models.Model):
    book = models.ForeignKey(LTB, related_name='quants', on_delete=models.CASCADE)
    is_first_edition = models.BooleanField("Ist Erstausgabe")

    class Meta:
        ordering = ['book', 'is_first_edition']
        permissions = [
            ('add_quant_on_site', "Can add Quants on the Site"),
        ]