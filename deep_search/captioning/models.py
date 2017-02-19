from __future__ import unicode_literals

from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-managed `created_at` and
    `modified_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'base'


class ImageCaptioning(TimeStampedModel):
    """
    Model to store the Image Captioning objects
    """
    image = models.ImageField(upload_to='image-captioning')
    caption = models.CharField(max_length=10000, null=True)

    def __unicode__(self):
        return self.caption

    class Meta:
        app_label = 'captioning'
        db_table = 'image_captioning'
