from django import forms
from django.core.exceptions import ValidationError

from ltb.models import LTBType, LTBNumber, LTBEditionNumber, LTB
from .models import Quant


class AddBookForm(forms.ModelForm):
    """
    TODO: Docstring
    """
    ON_STOCK_CHOICES = {
        (False, 'Nein'),
        (True, 'Ja')
    }

    ltb_type = forms.ModelChoiceField(label="Typ",
                                      queryset=LTBType.objects.all(),
                                      empty_label=None)
    ltb_number = forms.CharField(label="Nummer")
    ltb_edition = forms.ModelChoiceField(label="Auflage",
                                         queryset=LTBEditionNumber.objects.all(),
                                         empty_label=None)
    is_first_edition = forms.ChoiceField(label="Erstausgabe", choices=ON_STOCK_CHOICES)

    class Meta:
        """
        TODO: Docstring
        """
        model = Quant
        fields = ('ltb_type', 'ltb_number', 'ltb_edition', 'is_first_edition')

    def clean_ltb_number(self):
        """
        TODO: Docstring

        :return:
        """
        try:
            number = int(self.data['ltb_number'])
        except ValueError:
            raise ValidationError(
                '%(value)s ist keine Zahl',
                params={'value': self.data['ltb_number']})

        if number <= 0:
            raise ValidationError('Nummer muss größer als 0 sein.')

        ltb_number = LTBNumber.objects.filter(number=number).first()
        if ltb_number:
            self.cleaned_data['ltb_number'] = ltb_number
            return ltb_number
        else:
            raise ValidationError(
                'Nummer %(value)s ist nicht vorhanden',
                params={'value': str(number).zfill(3)})

    def clean(self):
        """
        TODO: Docstring

        :return:
        """
        if self.cleaned_data.get('ltb_edition') and self.cleaned_data.get('ltb_number') and self.cleaned_data.get(
                'ltb_type'):
            book = LTB.objects.filter(
                ltb_edition__ltb_edition_number=self.cleaned_data['ltb_edition'],
                ltb_edition__ltb_number_set__ltb_number=self.cleaned_data['ltb_number'],
                ltb_edition__ltb_number_set__ltb_type=self.cleaned_data['ltb_type']).first()
            if book:
                self.cleaned_data['book'] = book
                return self.cleaned_data
            else:
                raise ValidationError('Buch existiert nicht')

    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        if commit:
            quant = Quant(book=self.cleaned_data.get('book'),
                          is_first_edition=self.cleaned_data.get('is_first_edition'))
            quant.save()
            return quant
        return None
