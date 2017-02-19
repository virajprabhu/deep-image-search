from nltk.tokenize import word_tokenize

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

# from chat.sender import vqa_sender
from chat.utils import log_to_terminal

import chat.constants as constants
import uuid
import os
import traceback
import random
import urllib2
import numpy as np
import gensim
import nltk
import pickle
import string
from annoy import AnnoyIndex

print "Loading word2vec..."
w2v = gensim.models.Word2Vec.load_word2vec_format("data/GoogleNews-vectors-negative300.bin", binary=True)

print "Loaded successfully"
t = AnnoyIndex(300, metric='euclidean')
t.load("data/index.ann")    
ix2imid = pickle.load(open("data/ix2imid.p", "rb"))
print ix2imid

def compute_score(caption):
    words = parse_sen(caption)
    count = 0
    caption_score = np.zeros(300)
    for ix, word in enumerate(words):
        if word in w2v:
            caption_score += w2v[word]
            count += 1
    if count == 0:
        return caption_score
    return caption_score / float(count)


def parse_sen(sentence):
    valid_chars = string.ascii_letters + string.digits + '  '
    sentence = ''.join(c for c in sentence if c in valid_chars)
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    sen_wordlist = []
    for item in tagged_sentence:
        if item[1][0] == 'N' or item[1][0] == 'V' or item[1][0] == 'J' or item[1][:2] == 'RB':
            sen_wordlist.append(item[0])
    result = sen_wordlist
    return result


def home(request, template_name="chat/index.html"):
    socketid = uuid.uuid4()
    image_list = constants.LIST_OF_IMAGES
    caption_list = constants.LIST_OF_CAPTIONS
    query = ''
    if request.method == "POST":
        try:
            socketid = request.POST.get("socketid")
            query = request.POST.get("query")

            score = compute_score(query)
            nns = t.get_nns_by_vector(score, 5)

            closest_images = [ix2imid[ix] for ix in nns]
            closest_captions = [caption_list[ix] for ix in nns]

            image_list = closest_images
            caption_list = closest_captions
        except Exception, err:
            print str(err)

    image_path_list = [os.path.join(settings.STATIC_URL, 'images', 'val2014', image_id + '.jpg') for image_id in image_list]
    image_caption_list = zip(image_path_list, caption_list)

    return render(request, template_name, {"socketid": socketid, "image_path_list": image_caption_list, 'query': query})


def upload_image(request):
    if request.method == "POST":
        image = request.FILES['file']
        socketid = request.POST.get('socketid')
        output_dir = os.path.join(settings.MEDIA_ROOT, 'svqa', socketid)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        img_path = os.path.join(output_dir, str(image))
        handle_uploaded_file(image, img_path)
        img_url = img_path.replace(settings.BASE_DIR, "")
        print request.POST
    return JsonResponse({"file_path": img_path, "img_url": img_url})


def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
