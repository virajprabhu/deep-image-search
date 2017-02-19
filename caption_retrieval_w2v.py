import json
import gensim
import numpy
import pickle
import nltk
import numpy as np
import string
from annoy import AnnoyIndex

data = []
w2v = {}

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
	valid_chars = string.ascii_letters + string.digits + ' 	'
	sentence = ''.join(c for c in sentence if c in valid_chars)
	tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
	sen_wordlist = []
	for item in tagged_sentence:
		if item[1][0] == 'N' or item[1][0] == 'V' or item[1][0] == 'J' or item[1][:2] == 'RB':
			sen_wordlist.append(item[0])
	result = sen_wordlist
	return result

def main():
	global w2v
	with open("picked_images_allcap.json", "r") as f:
		annotations = json.loads(f.read())
		captions = [ann["pred_cap"] for ann in annotations]
		image_ids = [ann["image"] for ann in annotations]

	print "Loading word2vec..."
	w2v = gensim.models.Word2Vec.load_word2vec_format("../word2vec.torch/GoogleNews-vectors-negative300.bin", binary=True)
 
	print "Loaded successfully"
	caption_score_list, caption_list = [], []
	t = AnnoyIndex(300, metric="euclidean")
	ix2imid = {}
	skipped = 0
	for ix, caption in enumerate(captions):
		if ix%500 == 0:
			print str(ix) + " / " + str(len(captions))
		
		score = compute_score(caption)

		if not np.any(score):
			skipped += 1
		else:
			caption_list.append(caption)
			caption_score_list.append(score)
			t.add_item(ix-skipped, score)
			ix2imid[ix-skipped] = image_ids[ix]

	print "Skipped ", skipped
	t.build(10)
	t.save("index.ann")
	# t.load("index.ann")

	pickle.dump( ix2imid, open("ix2imid.p", "wb") )
	# while True:
	# 	ip_caption = raw_input('--> ')
	# 	score = compute_score(ip_caption)
	# 	nns = t.get_nns_by_vector(score, 5)
	# 	closest_captions = [caption_list[i] for i in nns]
	# 	print closest_captions

if __name__ == "__main__":					
	main()