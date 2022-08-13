from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django import forms

from .models import User, Province, Address

class CustomUserCreationForm(UserCreationForm):

    class Meat:
        model = User
        fields = ('email',)
        field_classes = {"email": UsernameField}


class CustomUserChangeForm(UserChangeForm):

    class Meat:
        model = User
        fields = ('email',)


class UserSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        # print(self.fields)
        for f in self.fields.values():
            f.widget.attrs.update({'class':'form-control'}) #boot strap
        self.fields['email'].widget.attrs.update({'autocomplete': 'username', 'autofocurs': True})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class AddressForm(forms.ModelForm):

    province = forms.ChoiceField(choices=Province.objects.all().values_list('id','name'))
    
    class Meat:
        model = Address
        fields = ('province','city','address','postal_code')

    class Media:
        js = ('CustomUser/js/addAddress.js',)