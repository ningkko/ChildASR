#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
# import config 
import pickle
import sys
import os
import tqdm

import src.cha_util as cha_util
from src.pylangacq.chat import *
from src.pylangacq.dependency import *
from src.pylangacq.measures import *
from src.pylangacq.util import *

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import math
import string
import json
from pattern.text.en import singularize


# import argparse

# import enchant

# from nltk.corpus import words
# nltk_eng_dict = set(words.words())

def calc_freq(words):
    """
    :param: a list of words
    :output: a pandas dataframe of unique words and their frenquencies 
    """
    _dict = Counter(words)
    _dict = dict(sorted(_dict.items(), key=lambda item: item[1], reverse=True))
    
    df = pd.DataFrame(list(_dict.items()))
    df.columns = ["word","count"]
    return df

def find_eng_words(words):
    """
    :param: a list of words
    :output: a pandas dataframe of unique english words and their frenquencies 
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

def count_utterance_freq(utterances):
    """
    :param: a list of utterances
    :output: a pandas dataframe of unique utterances and their frenquencies 
    """

    _dict=Counter(utterances)
    _dict = dict(sorted(_dict.items(), key=lambda item: item[1], reverse=True))
    
    df = pd.DataFrame(list(_dict.items()))
    df.columns = ["utterance","count"]
    return df

def get_utterances_from_cha(corpus_name):
    """
    This function reads all .cha files for a corpus and return all utterance including punctuations
    :return: all utterances (non-unique) appear in a corpus
    """
    all_utterance = []

    file_path = corpus_name+"/*.cha"
    files = glob.glob(file_path)

    pbar = tqdm.tqdm(total=len(files))

    for file in files:
        eve = read_chat(file)
        #get all participants
        pars = list(eve.participant_codes())
        for p in pars:
            if p!= "CHI":
                utts = [k[1] for k in eve.utterances(participant=p)]
                clean_utts = []
                for sentence in utts:
                    clean_sent = cha_util.extract_words(sentence)
                    if clean_sent:
                        clean_utts.append(clean_sent)
                all_utterance += clean_utts
                
        pbar.update(1)
    # print(all_utterance)
    output_filename = "src/words/"+corpus_name+"_utt.txt"

    with open(output_filename,"w") as file:
        file.writelines("\n".join(all_utterance))

    return all_utterance

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

def get_utterance(corpus_name):

    all_utterance = get_utterances_from_cha(corpus_name)
    utterance_freq = count_utterance_freq(all_utterance)

    print("%s contains %i utterances."%(corpus_name, utterance_freq["count"].sum()))
    return all_utterance

def get_words(corpus_name):

    all_words = get_words_from_cha(corpus_name)
    # word_freq = find_eng_words(all_words)
    word_freq = calc_freq(all_words)
    output_filename = corpus_name+"_word_freq.csv"
    word_freq.to_csv("src/words/"+output_filename,index=False)

    print("%s contains %i words."%(corpus_name, word_freq["count"].sum()))
    return all_words

def find_freq_dist(voc_size):
    """
    :@param: dictionaries of child voc size distributions
    """

    dist = Counter([v for k,v in voc_size.items()])
    dist = {k: v for k, v in sorted(dist.items(), key=lambda item: item[0])}
    x = [k for k,v in dist.items()]
    y = [v for k,v in dist.items()]
    
    return x,y

def find_lim(a,b):
    """
    :@param: lists of ints
    """
    return int(min(a+b)), int(max(a+b))

def plot(voc_size1, voc_size2):

    """
    :@param: dictionaries of child voc size distributions
    :@return: lineplots
    """
    x1,y1 = find_freq_dist(voc_size1)
    plt.plot(x1, y1, label = "Typical Developing Kids", linewidth=0.6)
    
    x2,y2 = find_freq_dist(voc_size2)
    plt.plot(x2, y2, label = "Bilingual Kids", linewidth=0.6)
    print(x2)
    print(y2)
    
    plt.xlabel('Vocabulary sizes')
    plt.ylabel('Number of kids')
    plt.title('Child Vocabulary Distribution')
    
    x_min,x_max = find_lim(x1,x2)
    print(x_min,x_max)
    y_min,y_max = find_lim(y1,y2)

    plt.xticks([x_min,x_min+(x_max-x_min)/2,x_max])
    plt.yticks([0, y_max/2,y_max])

    plt.legend()
    plt.savefig("analysis/result.png",dpi=100)

    plt.show()
    
def generate_original_corpus(CORPUS_0_FREQ_PATH, CORPUS_0_PATH):
    """
    generates a list of sentences given the freqency file 

    ## This takes ~3 hr
    """
    df = pd.read_csv(CORPUS_0_FREQ_PATH).dropna()
    corpus_0 = np.array([])

    pbar = tqdm.tqdm(total=len(df))

    for index, content in df.iterrows():
        sentence = content[0]
        freq = content[1]
        corpus_0 = np.append(corpus_0,[content]*freq)
        pbar.update(1)

    corpus_0 = list(corpus_0)

    with open(CORPUS_0_PATH, "w") as file:
        file.writelines(corpus_0)

    return corpus_0


def sample_w_replacement(corpus):
    """
    :@param: a list of utterances
    :@return: a new list of utterances 
    """
    n = len(corpus)
    return np.random.choice(corpus,n)


def corpus_to_words(corpus):
    """
    given a corpus, return a dictionary of unique words and their frequencies
    :@param: a list of utterances
    :@return: a dictionary of unique words
    """
    words = []
    for sent in corpus:
        sent = sent.replace("\'s","").lower().split(" ")
        words += sent

    words_dict = Counter(words)
    words_dict = {k: v for k, v in sorted(words_dict.items(), key=lambda item: item[1])}
    words_dict = {key:val for key, val in words_dict.items() if val > 10}
    # with open("src/words/dev_freq.json","w") as file:
        # json.dump(words_dict,file,indent=4)

    return words_dict


def learn_vocabulary_size(corpus, learning_rate):
    '''
    Given a corpus and a learning rate, return learned words
    '''

    learned_voc = []
    # pbar = tqdm.tqdm(total=len(corpus))

    for word, freq in corpus.items():
        probability = 1-math.pow((1-learning_rate),freq)

        if probability >= 0.997:
            learned_voc.append(word)
        # pbar.update(1)

    return learned_voc


