from tkinter import image_names
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.urls import reverse

import inspect
from PIL import Image
import string
import random
import os
from typing import Dict
import json


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    date_created = models.DateTimeField(default=timezone.now, verbose_name=_('Date created'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Parent'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    def get_children(self):
        return Category.objects.filter(parent=self)

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'description': self.description,
            'parent': self.parent.pk if self.parent else None,
        }


class Brand(models.Model):
    name = models.CharField(_("name"),max_length=120,blank=False,null=False)
    about = models.TextField(_("about"),blank=True,null=True)
    website = models.CharField(_("website"),max_length=120,blank=False,null=False)
    date_created = models.DateTimeField(verbose_name=_("date created"),default=timezone.now)
    date_updated = models.DateTimeField(verbose_name=_("date updated"),auto_now=True)
    
    def get_absolute_url(self):
        return reverse("brand", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name

    def to_json(self) -> dict:
        return {
            'id': self.pk,
            'name': self.name,
            'about': self.about,
            'website': self.website,
        }


class Models(models.Model):
    firstname = models.CharField(_("fist name"), max_length=120, blank=True, null=False)
    lastname = models.CharField(_("last name"), max_length=120, blank=True, null=False)
    height = models.CharField(_("height"), max_length=120, blank=True, null=False)
    weight = models.CharField(_("weight"), max_length=120, blank=True, null=False)
    bust = models.CharField(_("bust"), max_length=120, blank=True, null=False)
    waist = models.CharField(_("waist"), max_length=120, blank=True, null=False)
    hip = models.CharField(_("hip"), max_length=120, blank=True, null=False)
    image = models.ImageField(upload_to='shop/models/%Y/%m/%d', verbose_name=_('Image'), blank=True, null=True)
    image_alt = models.CharField(max_length=200, verbose_name=_('Image alt'), blank=True, null=True)
    quick_add = models.TextField(_("quick add"), blank=True, null=True, help_text=_("add in the following format: <field name>:<value>.\nadd each field in one line"))
    date_created = models.DateTimeField(verbose_name=_("date created"), default=timezone.now)
    date_updated = models.DateTimeField(verbose_name=_("date updated"), auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if self.quick_add:
            for line in self.quick_add.splitlines():
                field, value = line.split(':')
                try:
                    getattr(self, field.lower())
                    setattr(self, field.lower(), value.strip())
                except:
                    print(f"{field} is not a valid field")
        self.quick_add = ''
        super(Models, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super(Models, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        verbose_name = _('Model')
        verbose_name_plural = _('Models')

    def get_absolute_url(self):
        return reverse('model', kwargs={'pk': self.pk})

    def to_json(self) -> Dict:
        return {
            'id': self.pk,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'height': self.height,
            'weight': self.weight,
            'bust': self.bust,
            'waist': self.waist,
            'hip': self.hip,
            'image': self.image.url if self.image else None,
        }

class SizeChoices(models.Model):
    name = models.CharField(_("name"), max_length=200, blank=False, null=False)
    bust = models.CharField(_("bust"), max_length=20, blank=False, null=False)
    waist = models.CharField(_("waist"), max_length=20, blank=False, null=False)
    hip = models.CharField(_("hip"), max_length=20, blank=False, null=False)
    date_created = models.DateTimeField(verbose_name=_("date created"), default=timezone.now)

    class Meta:
        verbose_name = _('Size Choice')
        verbose_name_plural = _('Size Choices')

    def __str__(self) -> str:
        return self.name

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'bust': self.bust,
            'waist': self.waist,
            'hip': self.hip,
        }

class ClotheSizeInfo(models.Model):
    fit = models.CharField(_("fit"), max_length=200, blank=True, null=True)
    length = models.CharField(_("length "), max_length=200, blank=True, null=True)
    bust = models.CharField(_("bust"), max_length=200, blank=True, null=True)
    waist = models.CharField(_("waist"), max_length=200, blank=True, null=True)
    hip = models.CharField(_("hip"), max_length=200, blank=True, null=True)
    undergarments = models.CharField(_("undergarments"), max_length=200, blank=True, null=True)
    fabric = models.CharField(_("fabric"), max_length=200, blank=True, null=True)
    quick_add = models.TextField(_("quick add"), blank=True, null=True, help_text=_("add in the following format: <field name>:<value>.\nadd each field in one line"))

    class Meta:
        verbose_name = _('Clothe Size Info')
        verbose_name_plural = _('Clothe Size Info')

    def save(self, *args, **kwargs) -> None:
        if self.quick_add:
            for line in self.quick_add.splitlines():
                field, value = line.split(':')
                try:
                    getattr(self, field.lower())
                    setattr(self, field.lower(), value.strip())
                except:
                    print(f"{field} is not a valid field")
        self.quick_add = ''
        super(ClotheSizeInfo, self).save(*args, **kwargs)

    def get_all(self):
        return [x for x in inspect.getmembers(self) if not x[0].startswith('__') and isinstance(x[1], str)]

    def __str__(self) -> str:
        return f"{self.fit}"

    def to_json(self) -> dict:
        return {
            'id': self.pk,
            'fit': self.fit,
            'length': self.length,
            'bust': self.bust,
            'waist': self.waist,
            'hip': self.hip,
            'undergarments': self.undergarments,
            'fabric': self.fabric,
        }


class ItemImage(models.Model):
    image = models.ImageField(upload_to='shop/items/%Y/%m/%d', verbose_name=_('Image'))
    image_alt = models.CharField(max_length=200, verbose_name=_('Image alt'), null = True)
    image_name = models.CharField(max_length=200, verbose_name=_('Image name'), blank= True, null = True)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def upload_image(self, *args, **kwargs) -> None:
        print(self.image, self.image.path, self.image.url)
        image = self.image
        path = str(image.path)
        new_image = Image.open(path)
        rnd_string = f'_{self.random_string()}.webp'
        if self.image_name is None:
            new_path = path[:path.rfind('.')] + rnd_string
            self.image_name = new_path[new_path.rfind('\\')+1:-5]
        else:
            new_path = path[:path.rfind('\\')+1] + self.image_name + rnd_string 
        new_image.save(new_path,'webp')
        image.name = image.name[:image.name.rfind('/')+1] + new_path[new_path.rfind('\\')+1:]
        print('image:',image)
        super(ItemImage, self).save(*args, **kwargs)
        os.remove(path)

    def save(self, *args, **kwargs) -> None:
        print(f'saving image: {self.pk}, {self.image}')
        print(args, kwargs)
        if self.pk is not None:
            old_one = ItemImage.objects.get(pk = self.pk)
            if old_one.image != self.image:
                super(ItemImage, self).save(*args, **kwargs)
                self.upload_image()
                os.remove(old_one.image.path)
            elif old_one.image_name != self.image_name:
                print('renaming')
                path = old_one.image.path
                rnd_string = f'_{self.random_string()}.webp'
                new_path = path[:path.rfind('\\')+1] + self.image_name + rnd_string
                os.rename(old_one.image.path, new_path)
                self.image.name = self.image.name[:self.image.name.rfind('/')+1] + new_path[new_path.rfind('\\')+1:]
                super(ItemImage, self).save(*args, **kwargs)
            else:
                super(ItemImage, self).save(*args, **kwargs)
        else:
            print('New image')
            super(ItemImage, self).save(*args , **kwargs)
            self.upload_image()

    def delete(self, *args, **kwargs):
        path = self.image.path
        print(f'Deleting {self.image.path}')
        super(ItemImage, self).delete(*args, **kwargs)
        os.remove(path)

    def random_string(self, n=6) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(n))

    def __str__(self):
        # return self.image.name[self.image.name.rfind('/')+1:]
        return self.image_name

    def to_json(self):
        return {
            'image': self.image.name,
            'image_url': self.image.url,
            'image_alt': self.image_alt,
            'image_name': self.image_name
        }
    

class Discount(models.Model):
    name = models.CharField(_("name"), max_length=200, blank=False, null=False)
    percent = models.PositiveIntegerField(_("percent"), blank=False, null=False)
    code = models.CharField(_("code"), max_length=10, blank=False, null=False)
    date_created = models.DateTimeField(verbose_name=_("date created"), default=timezone.now)
    date_expired = models.DateTimeField(verbose_name=_("date expired"), blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} {self.percent}%'

class Color(models.Model):
    name = models.CharField(_('name'), max_length= 100, blank= False, null= False)
    hex_code_validator = RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$', message="Hex code must be in the format #RRGGBB")
    color_code = models.CharField(max_length=7, validators=[hex_code_validator], verbose_name=_('color code'))

    def __str__(self) -> str:
        return f'{self.name}'

    def to_json(self) -> dict:
        return {
            'id': self.pk,
            'name': self.name,
            'color_code': self.color_code
        }

class Item(models.Model):
    name = models.CharField(_('name'), max_length=150, blank= False, null= False)
    page_title = models.CharField(_('page title'), max_length=150, blank= True, null= True)
    price = models.PositiveIntegerField(_('price'), blank= False, null= False)
    quantity = models.PositiveIntegerField(_('quantity'), blank= False, null= False, help_text=_("the number of items left in the stock"))
    color = models.ForeignKey(Color, on_delete=models.DO_NOTHING, verbose_name=_('color'))
    specific_color = models.CharField(_('specific color'), max_length=100, blank= True, null= True)
    category = models.ManyToManyField(Category, verbose_name=_('category'))
    rate = models.CharField(_("rate"), max_length=4, default="0")
    rate_count = models.IntegerField(_("rate count"), default=0)
    date_created = models.DateTimeField(verbose_name=_("date created"), default=timezone.now)
    date_updated = models.DateTimeField(verbose_name=_("date updated"), auto_now=True)

    def save (self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        if self.rate_count == 0:
            self.rate = "0"
        else:
            self.rate = str(round(self.rate_count / self.rate_count, 1))
        if self.specific_color is None:
            self.specific_color = self.color.name
        super(Item, self).save(*args, **kwargs)

    def to_json(self, exclude: list[str] = ['page_title','date_created','date_updated']):
        data = {}
        for field in self._meta.get_fields():
            if field.name not in exclude:
                if field.get_internal_type == 'ManyToManyField':
                    data[field.name] = [item for item in getattr(self, field.name).all()]
                else:
                    data[field.name] = str(getattr(self, field.name))
        return data

    class Meta:
        abstract = True

class Dress(Item):
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, verbose_name=_('brand'))
    images = models.ManyToManyField(ItemImage, verbose_name=_("images"))
    sizes = models.ManyToManyField(SizeChoices, verbose_name=_("available sizes"))
    sizeinfo = models.ForeignKey(ClotheSizeInfo, on_delete=models.DO_NOTHING)
    desc = models.TextField(_("description"), blank=True, null=True)
    features =  models.TextField(_("features"), blank=True, null=True, help_text=_("insert each feature in one line"))
    model = models.ForeignKey(Models, on_delete=models.DO_NOTHING, verbose_name=_("model"))
    related = models.ManyToManyField('self', verbose_name=_('related items'), blank=True)
    add_related = models.TextField(_("add related items"), blank=True, null=True, help_text=_("insert each item in one line"))

    def save(self, *args, **kwargs):
        if self.add_related:
            dresses = self.parse_add_related()
            self.add_related = ''
            super(Dress, self).save(*args, **kwargs)
            dresses.append(Dress.objects.get(pk=self.pk))
            print(f'len of dresses: {len(dresses)}')
            for dress in dresses:
                print('D:', dress)
                for dress1 in dresses:
                    if dress != dress1:
                        print('\t', dress1)
                        dress.related.add(dress1)
                dress.related.add()
                dress.save()
        super(Dress, self).save(*args, **kwargs)

    def parse_add_related(self) -> list['Dress']:
        dresses: list[Dress] = []
        for line in self.add_related.splitlines():
            if line.startswith('# '): #New Dress name
                dresses.append(Dress(name=line[2:]))
            else:
                dresses[-1].cat_flag = False
                dresses[-1].size_flag = False
                key, value = map(self.to_lower,line.split(':'))
                if key == 'price':
                    dresses[-1].price = int(value)
                elif key == 'quantity':
                    dresses[-1].quantity = int(value)
                elif key == 'color':
                    print('color: ',value.capitalize())
                    dresses[-1].color = Color.objects.get(name=value.capitalize())
                elif key == 'specific color':
                    dresses[-1].specific_color = value
                elif key == 'category':
                    dresses[-1].cat_flag = values
                elif key == 'sizes':
                    dresses[-1].size_flag = value
                elif key == 'sizeinfo':
                    dresses[-1].sizeinfo = ClotheSizeInfo.objects.get(name=value)
                elif key == 'model':
                    dresses[-1].model = Models.objects.get(firstname=value.capitalize())
        fields = self._meta.fields
        for dress in dresses:
            for field in fields[1:]:
                try:
                    val = getattr(dress, field.name)
                    if val is None:
                        setattr(dress, field.name, getattr(self, field.name))
                except:
                    setattr(dress, field.name, getattr(self, field.name))
            dress.add_related = ''
            dress.save()
            if dress.cat_flag:
                values = dress.cat_flag.split(',')
                for value in values:
                    dress.category.add(Category.objects.get(name=value.strip().capitalize()))
            else:
                for cat in self.category.all():
                    dress.category.add(cat)
            if dress.size_flag:
                values = dress.size_flag.split(',')
                print("SIZE CHOICES")
                for value in values:
                    value = value.strip().upper()
                    print('value:', value)
                    dress.sizes.add(SizeChoices.objects.get(name=value))
            else:
                for size in self.sizes.all():
                    dress.sizes.add(size)
            dress.save()
        return dresses

    def __str__(self) -> str:
        return f'{self.name}'

    def to_json(self, exclude: list[str] = []) -> dict:
        if exclude:
            data = super().to_json(exclude)
        else:
            data = super().to_json()
        for field in self._meta.get_fields():
            if field.name not in exclude:
                if field.name == 'related':
                    data['related'] = [{'id': item.pk, 'name': item.name} for item in self.related.all()]
                    continue
                if field.get_internal_type() == 'ManyToManyField':
                    inner_data = []
                    for item in getattr(self, field.name).all():
                        inner_data.append(item.to_json())
                    data[field.name] = inner_data
                elif field.get_internal_type() == 'ForeignKey':
                    data[field.name] = getattr(self, field.name).to_json()
                else:
                    data[field.name] = str(getattr(self, field.name))
        return data

    def to_lower(self, value: str) -> str:
        return value.lower().strip()

classes: list[models.Model] = {'Dress': Dress, 'Item': Item, 'Category': Category, 'Color': Color, 'Models': Models, 'SizeChoices': SizeChoices,
'ClotheSizeInfo': ClotheSizeInfo, 'ItemImage': ItemImage}