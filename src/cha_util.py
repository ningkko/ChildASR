import string
import re
from nltk.corpus import words
nltk_eng_dict = set(words.words())
# from pattern.text.en import singularize
# from nltk.stem.snowball import SnowballStemmer

def clean(word, stemmer):
    

    in_word_symbols = ["0","„","\"","(",")",":","?","!","ˌ","ˈ","^","&-","/","=","*",",","...","..","."," "]
    for symbol in in_word_symbols:
        if symbol in word:
            word = word.replace(symbol,"")
    if stemmer:
        word = stemmer.stem(word)
    return word
    # # uncomment this for english
    # if word in nltk_eng_dict:
        # return word

def extract_words(sentence, stemmer):
    """
    See chapter 8 of the CHAT format paper
    """
    clean_words = []

    pass_symbols = ["+/.","+//","//.","+//.","@l","xxx","yyy","www","+<","+..."]
    sentence = sentence.split(" ")

    # for repetitions
    previous_word = ""

    for word in sentence:
        if word in string.punctuation:
            continue
        for ps in pass_symbols:
            if ps in word:
                continue

        # pause
        if "(" in word and "." in word and ")" in word:
            continue
        # repetition
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
                clean_words.append(clean(w, stemmer))
            continue
        elif "+" in word:
            for w in word.split("+"):
                clean_words.append(clean(w, stemmer))
            continue
        if "@" in word:
            clean_words.append(clean(word.split("@")[0], stemmer))
            continue

        word = clean(word,stemmer)

        # if "+" in word:
            # print(word)
        if word:
            clean_words.append(word)
        previous_word = word

    return " ".join(clean_words)







