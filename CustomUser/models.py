from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator
from django.urls import reverse

from .managers import CustomUserManager
from .fit_choices import *
from shop.models import Kala

class Province(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(_('name'), max_length=50, blank=False, null=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='cities', blank=False)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return f'{self.name} - {self.province.name}'

class Address(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False)
    address = models.CharField(max_length=150, blank=False)
    code_validator = RegexValidator(regex="^[0-9]{10}$",message=_("Please enter a valid postal code containning 10 numbers"))
    postal_code = models.CharField(_("postal code"),max_length=10,validators=[code_validator])
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, blank=False, related_name='the_user')
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    class Meta:
        verbose_name_plural = 'addresses'

    def get_absolute_url(self):
        return reverse('update_address', kwargs={'id': self.pk})
    
    def __str__(self):
        return f'{self.city}, {self.address}'

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'province': self.city.province.name,
            'city': self.city.name,
            'address': self.address,
            'postal_code': self.postal_code,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S')
        }


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    phone_validator = RegexValidator(regex="^[0-9]+$", message=_("Please enter a valid phone number containing 11 number"))
    phonenumber = models.CharField(_("phone number"), max_length=11, validators=[phone_validator],unique=True,blank=True,null=True)
    address = models.ManyToManyField(Address, blank=True, related_name='the_address')
    birthdate = models.DateField(_("birth date"), default=timezone.now, blank=True)
    bodytype = models.IntegerField(_("body type"), choices=BODYTYPE_CHOICES, blank=True, null=True)
    height = models.IntegerField(_("height"), choices=HEIGHT_CHOICES, blank=True, null=True, help_text=_("select your height in feet"))
    weight = models.IntegerField(_("weight"), blank=True, null=True, help_text=_("enter your weight in kg"))
    bust = models.IntegerField(_("bust"), choices=BUST_CHOICES, blank=True, null=True)
    waist = models.IntegerField(_("waist"), choices=WAIST_CHOICES, blank=True, null=True)
    hip = models.IntegerField(_("hip"), choices=HIP_CHOICES, blank=True, null=True)
    favorites = models.ManyToManyField(Kala, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        ordering = ['date_joined','last_name']

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'.title()
        return self.first_name

    def get_fit(self) -> dict:
        return {
            'bodytype': self.bodytype,
            'height': self.height,
            'weight': self.weight,
            'bust': self.bust,
            'waist': self.waist,
            'hip': self.hip
        }
    
    def save(self, *args, **kwargs):
        # if the address field is set, check that the choosen addresses' user is the same as the current user
        #TODO DOES NOT WORK
        super().save(*args, **kwargs)
        # if self.address.all():
        #     for address in self.address.all():
        #         print(address ,address.user)
        #         if address.user != self:
                    # raise ValueError('The address is not associated with the current user')