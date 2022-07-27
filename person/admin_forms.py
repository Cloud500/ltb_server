from django import forms

from .models import Person


class PersonForm(forms.ModelForm):
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(PersonForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = Person
        fields = ('name', 'description', 'type', 'url', 'image_url', 'image')
