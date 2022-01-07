from typing import Optional
from django import forms

from .models import LTB
from stock.models import Quant


class AddBookForm(forms.Form):
    """
    Form to add current book to inventory.

    Find/Add the book with the given slug and create a Quant
    """
    ON_STOCK_CHOICES = {
        (False, 'Nein'),
        (True, 'Ja')
    }
    first_edition = forms.ChoiceField(label="Erstausgabe", choices=ON_STOCK_CHOICES)
    slug = forms.CharField(widget=forms.HiddenInput())

    def clean(self) -> dict:
        """
        Adds the required records in the cleaning.

        :return: Dictionary of the cleaned form Data
        :rtype: dict
        """
        book = LTB.objects.get(slug=self.cleaned_data['slug'])
        self.cleaned_data['book'] = book
        return self.cleaned_data

    def save(self, commit: bool = True) -> Optional[Quant]:
        """
        Create a new Quant for the active book.

        :param commit: Create only if True
        :type commit: bool
        :return: the new Quant
        :rtype: Optional[Quant]
        """
        if commit:
            quant = Quant(book=self.cleaned_data.get('book'),
                          is_first_edition=self.cleaned_data.get('first_edition'))
            quant.save()
            return quant
        return None
