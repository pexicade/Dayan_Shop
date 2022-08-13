from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ItemImage

import os

@receiver(post_delete, sender=ItemImage)
def delete_image_files(sender, instance, using, **kwargs):
    path = instance.image.path
    if os.path.isfile(path):
        os.remove(path)