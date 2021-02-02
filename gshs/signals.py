from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
import os
from gshs.models import Photo, Repair


@receiver(post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)    
    # Photo.objects.get(pk=instance.pk).delete() 

@receiver(pre_save, sender=Photo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    old_file = Photo.objects.get(pk=instance.pk).image
    if old_file:
        new_file = instance.image
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        

    
   