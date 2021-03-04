import src.analyze as analyze
import pandas as pd
import numpy as np
from zipfile import ZipFile
import os
import json
import tqdm
import math

# CORPUS_0_PATH = "src/words/dev_utt.txt"
LEARNING_RATE = 0.1
CORPUS_0_PATH = "corpora/000.txt"


def _zip(original_file_path):
    """
    zip a file and delete the original one
    """
    original_file = original_file_path.split("/")[-1]
    filepath = "/".join(original_file_path.split("/")[:-1])
    # print(filepath)
    zipfile = original_file.replace(".json",".zip")

    os.chdir(filepath)
    ZipFile(zipfile, 'w').write(original_file)
    os.remove(original_file)
    os.chdir("../")


def generate_file_name(i):
    """
    :@param: int index i 
    :@return: file name
    """
    if 0<i<10:
        return "corpora/00"+str(i)+".json"
    elif 10<=i<100:
        return "corpora/0"+str(i)+".json"
    elif 100<=i<1000:
        return "corpora/"+str(i)+".json"

def main(): 

    if not os.path.exists(CORPUS_0_PATH):
        print("Run extract_utterance.py first")
        exit(1)
    else:
        with open(CORPUS_0_PATH, "r") as file:
            corpus_0 = file.read().split("\n")

    corpus_words = analyze.corpus_to_words(corpus_0)
    with open("corpora/000.json", "w") as file:
        json.dump(corpus_words,file,indent=4)
    _zip("corpora/000.json")
    learned_words = analyze.learn_vocabulary_size(corpus_words, LEARNING_RATE)

    print(len(learned_words))

    chi_dist = {0:len(learned_words)}
    
    # pbar = tqdm.tqdm(total=3)
    pbar = tqdm.tqdm(total=999)

    i = 1
    while i < 1000:
    # while i<4:
        # print(i)
        new_corpus_name = generate_file_name(i)
        # print(new_corpus_name)
        if os.path.exists(new_corpus_name):
            with open(new_corpus_name,"r") as file:
                corpus_words = json.load(file)
        else:
            new_corpus = analyze.sample_w_replacement(corpus_0)
            corpus_words = analyze.corpus_to_words(new_corpus)

            with open(new_corpus_name, "w") as file:
                json.dump(corpus_words,file,indent=4)
            _zip(new_corpus_name)

        learned_words = analyze.learn_vocabulary_size(corpus_words, LEARNING_RATE)

        chi_dist[i] = len(learned_words)
        pbar.update(1)
        i += 1

    with open("analysis/dev_child.json","w") as file:
        json.dump(chi_dist,file,indent=4)

main()










