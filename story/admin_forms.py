from django import forms

from .models import Story


class StoryForm(forms.ModelForm):
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(StoryForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = Story
        fields = (
            'code', 'title', 'genre', 'original_title', 'origin', 'date', 'pages', 'author', 'illustrator',
            'characters', 'url')
