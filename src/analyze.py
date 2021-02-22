import glob
# import config 
import pickle
import sys
import os
import tqdm


from src.pylangacq.chat import *
from src.pylangacq.dependency import *
from src.pylangacq.measures import *
from src.pylangacq.util import *

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import math
# import argparse

# import enchant

from nltk.corpus import words
nltk_eng_dict = set(words.words())

def find_eng_words(words):
    """
    :param: a list of words
    :output: a pandas dataframe of unique words and their frenquencies 
    """

    _dict={}

    l = Counter(words)
    for k,v in l.items():
        if k in nltk_eng_dict:
            _dict[k]=v

    _dict = dict(sorted(_dict.items(), key=lambda item: item[1], reverse=True))
    
    df = pd.DataFrame(list(_dict.items()))
    df.columns = ["word","count"]
    return df

def get_words_from_cha(corpus_name):
    """
    This function reads all .cha files for a corpus and return all words including punctuations
    :return: all words (non-unique) appear in a corpus
    """
    glob_par_list = []
    all_words = []

    file_path = corpus_name+"/*.cha"
    files = glob.glob(file_path)

    pbar = tqdm.tqdm(total=len(files))

    for file in files:
        # print(file)
        eve = read_chat(file)
        #get all participants
        pars = list(eve.participant_codes())
        for p in pars:
            if p!= "CHI":
                words = eve.words(participant=p)
                # print(words)
                if p not in glob_par_list:
                    glob_par_list.append(p)
                all_words += words
        pbar.update(1)

    with open(corpus_name+"_par.txt","w") as ff:
        ff.write(str(glob_par_list))

    return all_words

def get_words(corpus_name):

    all_words = get_words_from_cha(corpus_name)
    word_freq = find_eng_words(all_words)

    output_filename = corpus_name+"_word_freq.csv"
    word_freq.to_csv("src/words/"+output_filename,index=False)

    print("%s contains %i words."%(corpus_name, word_freq["count"].sum()))
    return all_words


def plot(corpus_name, words):

    """
    :param corpus_name: 
    :param words: 
    """

    if not os.path.isdir("analysis"):
        os.mkdir("analysis")

    plt.clf()

    l = int(len(_dict)*0.2)
    keys = words["word"][l:]
    values = words["count"][l:]
    
    plt.axes().set_ylim([0, int(math.ceil(max(values)*1.5))])
    plt.bar(keys, values)
    plt.xticks([])
    plt.xlabel("words")     
    plt.ylabel("freq") 
    plt.title(corpus_name+" word frequency distribution") 
    plt.savefig("analysis/"+corpus_name+".png")
    plt.show()
