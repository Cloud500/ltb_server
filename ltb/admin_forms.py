from django import forms

from .models import LTBType, LTBNumber, LTBNumberSet, LTBEditionNumber, LTBEdition, LTB


class LTBTypeForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBTypeForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBType
        fields = ('name', 'code', 'current_number', 'auto_url', 'type_url')


class LTBNumberForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBNumberForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBNumber
        fields = ('number',)


class LTBNumberSetForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBNumberSetForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBNumberSet
        fields = ('ltb_number', 'ltb_type', 'url')


class LTBEditionNumberForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBEditionNumberForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBEditionNumber
        fields = ('number',)


class LTBEditionForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBEditionForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBEdition
        fields = ('ltb_number_set', 'ltb_edition_number', 'url', 'title', 'stories', 'pages', 'release_date')


class LTBForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTB
        fields = ('ltb_edition', 'name', 'sort', 'image_url')
