from django import forms
from django.core.exceptions import ValidationError

from ltb.models import LTBType, LTBNumber, LTBEditionNumber, LTB
from .models import Quant


class AddBookForm(forms.ModelForm):
    ON_STOCK_CHOICES = {
        (False, 'Nein'),
        (True, 'Ja')
    }

    ltb_type = forms.ModelChoiceField(label="Typ",
                                      queryset=LTBType.objects.all(),
                                      empty_label=None)
    number = forms.CharField(label="Nummer")
    ltb_edition = forms.ModelChoiceField(label="Auflage",
                                         queryset=LTBEditionNumber.objects.all(),
                                         empty_label=None)
    first_edition = forms.ChoiceField(label="Ist Erstausgabe", choices=ON_STOCK_CHOICES)

    class Meta:
        model = Quant
        fields = ('ltb_type', 'number', 'ltb_edition', 'first_edition')

    def save(self, commit=True):
        message = {}
        valid_data = True
        new_data = dict(self.data)

        ltb_type_id = int(new_data.pop('ltb_type', [0, ])[0])
        ltb_edition_id = int(new_data.pop('ltb_edition', [0, ])[0])
        first_edition = bool(new_data.pop('first_edition', [False, ])[0])

        number = new_data.pop('number', [0, ])[0]
        try:
            number = int(number)
        except ValueError:
            valid_data = False
            message['success'] = False
            message['message'] = f"Eingabe ungültig"
            message['number'] = f"{number} ist keine Zahl"

        book = None
        if valid_data:
            book = LTB.objects.filter(
                ltb_edition__ltb_number_set__ltb_type__id=int(ltb_type_id),
                ltb_edition__ltb_number_set__ltb_number__number=number,
                ltb_edition__ltb_edition_number__id=int(ltb_edition_id)).first()
            if not book:
                message['success'] = False
                message['message'] = f"Es existiert kein Buch mit den angegebenen Daten"

        if commit and book:
            quant = Quant(book=book, is_first_edition=first_edition)
            quant.save()
            message['success'] = True
            message['message'] = f"\"{book.type}{book.number} - {book.complete_name}\" wurde hinzugefügt"
        else:
            message['success'] = False
        return message
