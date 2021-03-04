import string
import re
from nltk.corpus import words
nltk_eng_dict = set(words.words())
from pattern.text.en import singularize


def clean(word):
    in_word_symbols = ["0","„","\"","(",")",":","?","!","ˌ","ˈ","^","&-","/","=","*",",","...","..","."," "]
    for symbol in in_word_symbols:
        if symbol in word:
            word = word.replace(symbol,"")
    word = singularize(word)
    if word in nltk_eng_dict:
        return word
    return ""

def extract_words(sentence):
    """
    See chapter 8 of the CHAT format paper
    """
    clean_words = []

    pass_symbols = ["+/.","+//","//.","+//.","@l","xxx","yyy","www","+<","+..."]
    sentence = sentence.split(" ")
    previous_word = ""
    for word in sentence:
        if word in string.punctuation:
            continue
        for ps in pass_symbols:
            if ps in word:
                continue

        if "(" in word and "." in word and ")" in word:
            continue
        if "[/]" in word:
            clean_words.append(previous_word)
            continue
        if "[x" in word and "]" in word:
            n = word.split(" ").replace("]")
            if n:
                n = int(i)
            for i in range(n):
                clean_words.append(previous_word)
            continue

        ww = []
        if "_" in word:
            for w in word.split("_"):
                clean_words.append(clean(w))
            continue
        elif "+" in word:
            for w in word.split("+"):
                clean_words.append(clean(w))
            continue
        if "@" in word:
            clean_words.append(clean(word.split("@")[0]))
            continue

        word = clean(word)

        # if "+" in word:
            # print(word)
        if word:
            clean_words.append(word)
        previous_word = word

    return " ".join(clean_words)







