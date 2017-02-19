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
    intro_message = random.choice(constants.BOT_INTRODUCTION_MESSAGE)
    if request.method == "POST":
        try:
            socketid = request.POST.get("socketid")
            question = request.POST.get("question")
            # question = question.replace("?", "").lower()
            # img_path = request.POST.get("img_path")
            # history = request.POST.get("history", "")

            # img_path = urllib2.unquote(img_path)
            # abs_image_path = str(img_path)

            score = compute_score(question)
            nns = t.get_nns_by_vector(score, 5)
            closest_images = [ix2imid[ix] for ix in nns]
            
            # check if the question contains "?" at the end
            # q_tokens = word_tokenize(str(question))
            # if q_tokens[-1] != "?":
            #     question = "{0}{1}".format(question, "?")

            # response = vqa_sender(str(question), str(abs_image_path), socketid)
            log_to_terminal(socketid, {"show_images": closest_images})
        except Exception, err:
            log_to_terminal(socketid, {"terminal": traceback.print_exc()})

    return render(request, template_name, {"socketid": socketid, "bot_intro_message": intro_message })


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
