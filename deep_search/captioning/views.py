from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

import uuid
import os
import random
import traceback
import urllib2
import requests
from urlparse import urlparse
from django.http import HttpResponse


from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ImageCaptioning
from .sender import send_image_for_captioning
from .serializers import ImageCaptioningSerializer


@api_view(['GET', 'POST'])
def image_captioning_list(request):
    if request.method == 'GET':
        image_captioning_objects = ImageCaptioning.objects.all()
        serializer = ImageCaptioningSerializer(image_captioning_objects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ImageCaptioningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print serializer.data
            # send_image_for_captioning(image_path)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def image_captioning_detail(request, pk):
    """
    Retrieve a image_captioning instance.
    """
    try:
        image_captioning_obj = ImageCaptioning.objects.get(pk=pk)
    except ImageCaptioning.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ImageCaptioningSerializer(image_captioning_obj)
        return Response(serializer.data)


def captioning(request):
    socketid = uuid.uuid4()
    if request.method == "POST":
        try:
            img_path = request.POST.get('img_path')
            img_path = urllib2.unquote(img_path)
            caption = request.POST.get('caption', '')
            socketid = request.POST.get('socketid')

            abs_image_path = os.path.join(settings.BASE_DIR, str(img_path[1:]))
            out_dir = os.path.dirname(abs_image_path)

            # Run the captioning wrapper
            log_to_terminal(socketid, {"terminal": "Starting Captioning job..."})
            response = grad_cam_captioning(str(abs_image_path), str(caption), str(out_dir+"/"), socketid)
        except Exception, err:
            log_to_terminal(socketid, {"terminal": traceback.print_exc()})

    demo_images = get_demo_images(constants.COCO_IMAGES_PATH)
    return render(request, template_name, {"demo_images": demo_images, 'socketid': socketid})


def upload_image_using_url(request):
    if request.method == "POST":
        try:
            socketid = request.POST.get('socketid', None)
            image_url = request.POST.get('src', None)
            demo_type = request.POST.get('type')

            if demo_type == "vqa":
                dir_type = constants.VQA_CONFIG['image_dir']
            elif demo_type == "classification":
                dir_type = constants.CLASSIFICATION_CONFIG['image_dir']
            elif demo_type == "captioning":
                dir_type = constants.CAPTIONING_CONFIG['image_dir']

            img_name =  os.path.basename(urlparse(image_url).path)
            response = requests.get(image_url, stream=True)

            if response.status_code == 200:
                random_uuid = uuid.uuid1()
                output_dir = os.path.join(dir_type, str(random_uuid))

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                img_path = os.path.join(output_dir, str(img_name))
                with open(os.path.join(output_dir, img_name), 'wb+') as f:
                    f.write(response.content)

                img_path =  "/" + "/".join(img_path.split('/')[-5:])
                
                return JsonResponse({"file_path": img_path})
            else:
                return HttpResponse("Please Enter the Correct URL.")
        except:
            return HttpResponse("No images matching this url.")
    else:
        return HttpResponse("Invalid request method.")