import glob
# import config 
import pickle
import sys
import os

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

import enchant

def get_words(corpus_name):
    """
    This function reads all .cha files for a corpus and return all words including punctuations
    :return: all words (non-unique) appear in a corpus
    """
    glob_par_list = []
    all_words = []

    file_path = "src/prep/"+corpus_name+"/*.cha"
    files = glob.glob(file_path)
    
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
    
    with open("src/words/"+corpus_name+".pkl", 'wb') as f:
        pickle.dump(all_words, f)

    with open(corpus_name+"_par.txt","w") as ff:
        ff.write(str(glob_par_list))

    print("%s contains %i words including punctuations."%(corpus_name, len(all_words)))
    return all_words


def plot(corpus_name, words):

    # parser = argparse.ArgumentParser(description='preprocessing the data')
    # parser.add_argument('--input_path', type=str,
    #                     help='The path to xls file')
    # args = parser.parse_args()
    # input_file_name = args.input_path.split(".")[0]

    # with open(args.input_path, 'rb') as f:
    #     data = pickle.load(f)

    l = Counter(words)
    _dict={}

    # get rid of punctuations and non-eng words
    d = enchant.Dict("en_US")
    for k,v in l.items():
        if d.check(k):
            _dict[k]=v
    
    _dict = dict(sorted(_dict.items(), key=lambda item: item[1]))
    
    df = pd.DataFrame(list(_dict.items()))
    df.columns = ["word","count"]

    output_filename = corpus_name+"_word_freq.csv"

    if not os.path.isdir("analysis"):
        os.mkdir("analysis")
    df.to_csv("analysis/"+output_filename,index=False)

    plt.clf()

    keys = list(map(str,_dict.keys()))
    values = list(map(int,_dict.values()))
    
    plt.axes().set_ylim([0, int(math.ceil(max(values)*1.5))])
    plt.bar(keys, values)
    plt.xticks([])
    plt.xlabel("words")     
    plt.ylabel("freq") 
    plt.title(corpus_name+" word frequency distribution") 
    plt.savefig("analysis/"+corpus_name+".png")
    plt.show()
