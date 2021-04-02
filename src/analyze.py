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
import random
from scipy.stats import binom

from nltk.probability import FreqDist
import statistics
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
    output_filename = "corpora/"+corpus_name+"_000.txt"

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
    xs = [k for k,v in dist.items()]
    ys = [v for k,v in dist.items()]

    ### the following code finds the x where max y appears

    left_x, left_y = 0, 0
    right_x, right_y = 0, 0
    for x,y in zip(xs,ys):
        if y > right_y:
            left_y, right_y = y, y 
            left_x, right_x = x, x
        if y == right_y:      
            right_x = (x-left_x)/2+left_x
    median_x = right_x
    # ## find the median
    # index_dict = dict(zip(ys,xs))
    # # print(index_dict)
    # median_y = statistics.median(ys)
    # median_x = index_dict.get(median_y)

    # if not median_x:
    #     left_y = 0
    #     for x,y in zip(sorted(xs),sorted(ys)):
    #         if y < median_y:
    #             left_y = y
    #         else:
    #             break
    #     left_x = index_dict.get(left_y)
    #     right_x = index_dict.get(y)
    #     median_x = (left_x+right_x)

    return xs,ys,median_x

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
    x1,y1,median_1 = find_freq_dist(voc_size1)
    plt.plot(x1, y1, label = "Typical Developing Kids", linewidth=0.6)
    
    x2,y2,median_2 = find_freq_dist(voc_size2)
    plt.plot(x2, y2, label = "Bilingual Kids", linewidth=0.6)
    
    plt.xlabel('Vocabulary sizes')
    plt.ylabel('Number of kids')
    plt.title('Child Vocabulary Distribution')
    
    x_min,x_max = find_lim(x1,x2)
    y_min,y_max = find_lim(y1,y2)

    plt.xticks([x_min,x_min+(x_max-x_min)/2,x_max])
    plt.yticks([0, y_max/2,y_max])

    ## plot median

    plt.axvline(x=median_1,linewidth=0.5, color='gray', linestyle = "dashed")
    plt.text(median_1+1, y_max, str(median_1))
    plt.axvline(x=median_2,linewidth=0.5, color='gray', linestyle = 'dashed')
    plt.text(median_2+1, y_max, str(median_2))

    plt.legend()
    plt.savefig("analysis/result.png",dpi=200)

    plt.show()
    
def generate_original_corpus(CORPUS_0_FREQ_PATH, CORPUS_0_PATH):
    """
    generates a list of sentences given the freqency file 

    ## This takes ~3 hr
    """
    df = pd.read_csv(CORPUS_0_FREQ_PATH).dropna()
    corpus_0 = np.array([])

    for index, content in df.iterrows():
        sentence = content[0]
        freq = content[1]
        corpus_0 = np.append(corpus_0,[content]*freq)
        pbar.update(1)

    corpus_0 = list(corpus_0)

    with open(CORPUS_0_PATH, "w") as file:
        file.writelines(corpus_0)

    return corpus_0


# millions of words addressed to child 
def input_voc(month):
    '''finds the number of words a typical middle class child hears at a given age (in months)'''
    return int(0.625*month*1000000)

def sample_w_replacement(corpus, corpus_size):
    """
    :@param: a list of utterances
    :@return: a new list of utterances 
    """

    return np.random.choice(corpus,corpus_size)


def corpus_to_word_freq(corpus):
    """
    given a corpus, return a dictionary of unique words and their frequencies
    :@param: a list of utterances
    :@return: a dictionary of unique words
    """
    text = []
    for sentence in corpus:
        words = sentence.split(" ")
        if words:
            text+=words
    freq = FreqDist(text)
    freq.pop("",None)


    return freq


def learn_vocabulary_size(corpus, lr_dict, selected_words):
    '''
    Given a word_freq dictionary and a learning rate dictionary, return learned words
    '''
    selected_words_freq = {k: v for k, v in corpus.items() if k in selected_words}
    # print("%i word selected."%(len(selected_words_freq)))

    learned = []

    for k,v in selected_words_freq.items():
            prob = 1-binom.cdf(0, v, lr_dict[k])
            indicator = random.random()
            if indicator < prob:
                learned.append(k)

    # print("Learned %i words from %i sample words sampled from %i unique words"%(len(learned),len(selected_words_freq), len(corpus)))

    return selected_words_freq,learned


