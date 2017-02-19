from rest_framework import serializers

from .models import (ImageCaptioning,)
                     

class ImageCaptioningSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImageCaptioning
        fields = '__all__'
