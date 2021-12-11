from django import forms

from .models import LTBType, LTBNumber, LTBNumberSet, LTBEditionNumber, LTBEdition, LTB


class LTBTypeForm(forms.ModelForm):
    """
    TODO: Docstring
    """
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBTypeForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTBType
        fields = ('name', 'code', 'current_number', 'auto_url', 'auto_fetch', 'type_url')


class LTBNumberForm(forms.ModelForm):
    """
    TODO: Docstring
    """
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBNumberForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTBNumber
        fields = ('number',)


class LTBNumberSetForm(forms.ModelForm):
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBNumberSetForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTBNumberSet
        fields = ('ltb_number', 'ltb_type', 'url')


class LTBEditionNumberForm(forms.ModelForm):
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBEditionNumberForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTBEditionNumber
        fields = ('number',)


class LTBEditionForm(forms.ModelForm):
    """
    TODO: Docstring
    """
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBEditionForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTBEdition
        fields = ('ltb_number_set', 'ltb_edition_number', 'url', 'title', 'stories', 'pages', 'release_date')


class LTBForm(forms.ModelForm):
    """
    TODO: Docstring
    """
    def save(self, commit=True):
        """
        TODO: Docstring

        :param commit:
        :return:
        """
        instance = super(LTBForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        """
        TODO: Docstring
        """
        model = LTB
        fields = ('ltb_edition', 'name', 'sort', 'image_url', 'is_read')
