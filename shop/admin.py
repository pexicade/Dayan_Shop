from django.contrib import admin
from django.shortcuts import redirect, render

from .models import Category, Brand, Models, SizeChoices, ClotheSizeInfo, ItemImage, Color, Dress, testItem, Kala
from .forms import DressForm, ImageAdminForm

class DressAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'color', 'rate', 'quantity','date_updated')
    ordering = ('date_updated', 'name')

            
class ItemImageAdmin(admin.ModelAdmin):
    form = ImageAdminForm
    
    def save_model(self, request, obj, form, change) -> None:
        print('TYPE: ',type(obj))
        if change: #if an existing instance is being updated
            super(ItemImageAdmin, self).save_model(request, obj, form, change)
        else: #if a new instance is being created
            image_alt = obj.image_alt
            image_name = obj.image_name
            for image in request.FILES.getlist('image')[:-1]:
                instance = ItemImage(image=image, image_alt=image_alt, image_name=image_name)
                instance.save()
            obj.save()

    # def delete_queryset(self, request, queryset):
    #     super().delete_queryset(request, queryset)
    #     print(f'***DELETE Queryset***')
    #     for item in queryset:
    #         item.delete()


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Models)
admin.site.register(SizeChoices)
admin.site.register(ClotheSizeInfo)
admin.site.register(ItemImage,ItemImageAdmin)
admin.site.register(Color)
admin.site.register(Dress, DressAdmin)
admin.site.register(testItem)
admin.site.register(Kala)
