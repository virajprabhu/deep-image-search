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


class VQA(TimeStampedModel):
    """
    Model to store the VQA Request objects
    """
    image = models.ImageField()
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, null=True)

    def __unicode__(self):
        return self.question

    class Meta:
        app_label = 'vqa'
        db_table = 'vqa'
