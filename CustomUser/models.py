from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator
from django.urls import reverse

from .managers import CustomUserManager

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
    date_created = models.DateTimeField(_('date created'), default=timezone.now)

    class Meta:
        verbose_name_plural = 'addresses'

    def get_absolute_url(self):
        return reverse('update_address', kwargs={'id': self.pk})
    
    def __str__(self):
        return f'{self.city}, {self.address}'

BODYTYPE_CHOICES = [
    (0,'Athelic'),
    (1,'Curvey'),
    (2,'Hour glass'),
    (3,'Long and Lean'),
    (4,'Pear Shaped'),
    (5,'Petite'),
    (6,'Slender'),
]
HEIGHT_CHOICES = [
    (0,'4\' 6"'),(1,'4\' 7"'),(2,'4\' 8"'),(3,'4\' 9"'),(4,'4\' 10"'),(5,'5\' 0"'),
    (6,'5\' 1"'),(7,'5\' 2"'),(8,'5\' 3"'),(9,'5\' 4"'),(10,'5\' 5"'),(11,'5\' 6"'),
    (12,'5\' 7"'),(13,'5\' 8"'),(14,'5\' 9"'),(15,'5\' 10"'),(16,'6\' 0"'),
    (17,'6\' 1"'),(18,'6\' 2"'),(19,'6\' 3"'),(20,'6\' 4"'),(21,'6\' 5"'),
    (22,'6\' 6"'),(23,'6\' 7"'),(24,'6\' 8"'),(25,'6\' 9"'),(26,'6\' 10"'),
]

class User(AbstractUser):

    username = None
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    phone_validator = RegexValidator(regex="^[0-9]+$", message=_("Please enter a valid phone number containing 11 number"))
    phonenumber = models.CharField(_("phone number"), max_length=11, validators=[phone_validator],unique=True,blank=True,null=True)
    address = models.ManyToManyField(Address, blank=True)
    birthdate = models.DateField(_("birth date"), default=timezone.now, blank=True)
    bodytype = models.IntegerField(_("body type"), choices=BODYTYPE_CHOICES, blank=True, null=True)
    height = models.IntegerField(_("height"), choices=HEIGHT_CHOICES, blank=True, null=True, help_text=_("select your height in feet"))
    weight = models.IntegerField(_("weight"), blank=True, null=True, help_text=_("enter your weight in kg"))

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
        return ''