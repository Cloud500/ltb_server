from django import forms

from .models import LTBType, LTBNumberNumber, LTBNumberSet, LTBEditionNumber, LTBEdition, LTBSpecialEdition


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


class LTBNumberNumberForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBNumberNumberForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBNumberNumber
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
        fields = ('ltb_number_number', 'ltb_type', 'url')


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


class LTBSpecialEditionForm(forms.ModelForm):
    def save(self, commit=True):
        instance = super(LTBSpecialEditionForm, self).save(commit=commit)

        instance.slug = instance.create_slug()
        if commit:
            instance.save()
        return instance

    class Meta:
        model = LTBSpecialEdition
        fields = ('ltb_edition', 'name', 'sort', 'image_url')
