from dataclasses import fields
from django.forms import ModelForm
from django import forms
from .models import Dress, ItemImage
from django.utils.translation import gettext_lazy as _

class DressForm(ModelForm):
    class Meta:
        model = Dress
        fields = '__all__'

class ImageAdminForm(ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(ImageAdminForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'multiple':True})

    class Meta:
        model = ItemImage
        # fields = ['images','image_alt','image_name']
        fields = '__all__'
