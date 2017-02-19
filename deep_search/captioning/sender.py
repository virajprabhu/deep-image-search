from django.conf import settings

import os
import pika
import sys
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='image_captioning_task_queue', durable=True)

def send_image_for_captioning(image_path):

    global channel
    message = {
        'image_path': image_path,
    }
    channel.basic_publish(exchange='',
                      routing_key='image_captioning_task_queue',
                      body=json.dumps(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))

    print(" [x] Sent %r" % message)
