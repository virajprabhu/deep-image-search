from rest_framework import permissions, status
from rest_framework.decorators import (api_view,
                                       authentication_classes,
                                       permission_classes,
                                       throttle_classes,)
from rest_framework.response import Response

from .models import VQA
from .serializers import VQASerializer


@api_view(['GET', 'POST'])
def vqa(request):
    if request.method == 'GET':
        vqa_objects = VQA.objects.all()
        serializer = VQASerializer(vqa_objects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VQASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
