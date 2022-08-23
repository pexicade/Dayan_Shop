from email.policy import default
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from CustomUser.models import User
from shop.models import Kala, item_dct

import json

class Discount(models.Model):
    name = models.CharField(_("name"), max_length=200, blank=False, null=False)
    percent = models.PositiveIntegerField(_("percent"), blank=False, null=False)
    code = models.CharField(_("code"), max_length=10, blank=False, null=False)
    date_created = models.DateTimeField(verbose_name=_("date created"), default=timezone.now)
    date_expired = models.DateTimeField(verbose_name=_("date expired"), blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} {self.percent}%'

    def to_json(self) -> dict:
        return {
            'name': self.name,
            'percent': self.percent,
            'code': self.code,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'date_expired': self.date_expired.strftime('%Y-%m-%d %H:%M:%S') if self.date_expired else ''
        }

class OrderItem(models.Model):
    item = models.ForeignKey(Kala, on_delete=models.DO_NOTHING, blank=False)
    count = models.PositiveIntegerField(_("count"), blank=False, null=False)
    size = models.CharField(_("size"), max_length=25, blank=True, null=False)

    def get_model(self):
        # print(self.item.item_content_type)
        # model = ContentType.objects.get_for_model(self.item.item_content_type)
        x = str(self.item.item_content_type)
        x = x[x.rfind('|')+1:].strip()
        model = item_dct[x.title()]
        # print(model)
        return model

    def total_price(self) -> float:
        obj = self.get_model().objects.get(pk=self.item.item_id)
        return self.count * obj.price

    def get_name(self) -> str:
        return self.get_model().objects.get(pk=self.item.item_id).name

    def get_color(self) -> dict:
        return self.get_model().objects.get(pk=self.item.item_id).color.to_json

    # def get_size(self) -> dict:
    #     return self.get_model().objects.get(pk=self.item.item_id).sizes.to_json()

    def __str__(self) -> str:
        # model = self.get_model()/
        return f'{self.item.item_content_type} | {self.get_name()}'

    def get_details(self):
        print('d')
        return {
            'item': self.get_model().objects.get(pk=self.item.item_id).to_json(),
            'count': self.count,
            'total_price': self.total_price()
        }

    def save(self, *args, **kwargs):
        print(self.get_model().objects.get(pk=self.item.item_id).sizes.all())
        for s in self.get_model().objects.get(pk=self.item.item_id).sizes.all():
            if s.name == self.size:
                break
        else:
            raise Exception('size not found')
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.JSONField(_("address"), blank=True, null=False, default=dict)
    items = models.ManyToManyField(OrderItem, blank=False)
    items_detail = models.JSONField(blank=True, null=False, default=dict)
    total_count = models.PositiveIntegerField(blank=True, null=False,default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=False)
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=False)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=False)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    disount_detail = models.JSONField(blank=True, null=False, default=dict)
    price_after_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cancelled = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    data_completedd = models.DateTimeField(verbose_name=_("date completed"), blank=True, null=True)
    date_cancled = models.DateTimeField(verbose_name=_("date cancled"), blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_one = Order.objects.get(pk=self.pk)
            if old_one.cancelled or old_one.completed:
                raise Exception('Completed/Cancelled order cannot be changed')
        if self.cancelled and self.completed:
            raise Exception("An order can't be both cancelled and completed")
        if self.cancelled:
            self.date_cancled = timezone.now()
        if self.completed:
            self.data_completedd = timezone.now()
        if self.discount:
            if self.discount.date_expired and self.discount.date_expired < timezone.now():
                self.discount = None
                self.disount_detail = {}
                raise Exception(f'Discount was expired on {self.discount.date_expired.strftime("%Y-%m-%d %H:%M:%S")}')
            self.disount_detail = self.discount.to_json()
        super(Order, self).save(*args, **kwargs)
        self.total_count = sum([item.count for item in self.items.all()])
        self.total_price = sum([item.total_price() for item in self.items.all()])
        discount_percent = 0
        if self.discount:
            discount_percent = self.discount.percent
        self.price_after_discount = self.total_price * (100 - discount_percent) / 100
        details = {}
        for item in self.items.all():
            details[str(item)] = item.get_details()
            details[str(item)]['choosen_size'] = item.size
            # print(details[item])
            # if  item.size not in details['item']['sizes']:
            #     raise Exception(f'Size {item.size} is not available for {item.get_name()}')
        self.total_weight = sum([item['item']['weight'] * item['count'] for item in details.values()])
        print('DETAILS',details)
        self.items_detail = json.dumps({'total_count':self.total_count,'total_price': str(self.total_price),
                                       'price_after_discount':str(self.price_after_discount), 'total_weight':str(self.total_weight),
                                        'shipping_fee':get_shipping_fee(self.total_weight),'details':details})
        # self.address = self.user.address.to_json()
        super(Order, self).save(*args, **kwargs)


    # def __str__(self):
    #     return f'{self.content_type.name}'

def get_shipping_fee(weight: float) -> float:
    if weight < 250:
        return 5
    if weight < 500:
        return 7
    if weight < 750:
        return 9
    if weight < 1000:
        return 12
    if weight < 1500:
        return 16
    if weight < 2000:
        return 20
    return 25