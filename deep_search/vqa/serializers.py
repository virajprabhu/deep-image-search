from rest_framework import serializers

from .models import (VQA,)
                     

class VQASerializer(serializers.ModelSerializer):

    class Meta:
        model = VQA
        fields = '__all__'
