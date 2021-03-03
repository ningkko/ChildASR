import string
import re
from nltk.corpus import words
nltk_eng_dict = set(words.words())

UNINTELLIGIBLE_SPEECH = "xxx"
PHONOLOGICAL_CODING = "yyy"
UNTRANSCRIBED_MATERAL = "www"

def extract_words(sentence):
	"""
	See chapter 8 of the CHAT format paper
	"""
	clean_words = []
	
	omitted = ["0","(",")"]

	sentence = sentence.split(" ")
	for word in sentence:
		if word == UNTRANSCRIBED_MATERAL or word == PHONOLOGICAL_CODING or word == UNTRANSCRIBED_MATERAL:
			pass
		if "@l" in word:
			pass

		if "_" in word:
			clean_words += word.split("_")
		elif "+" in word:
			clean_words +=word.split("+")
		elif "@" in word:
			clean_words.append(word.split("@")[0])
		else:
			for symbol in omitted:
				if symbol in word:
					word = word.replace(symbol,"")
			clean_words.append(word)
	clean_eng_words = []

	for w in clean_words:
		if w and w not in string.punctuation and w in nltk_eng_dict:
			clean_eng_words.append(w) 

	return " ".join(clean_eng_words)









