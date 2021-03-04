import src.analyze as analyze
import pandas as pd
import numpy as np
from zipfile import ZipFile
import os

CORPUS_0_FREQ_PATH = "src/words/dev_utt_freq.csv"
CORPUS_0_PATH = "corpora/000.txt"
COPORA_DIR = "corpora"


def _zip(original_file):
    """
    zip a file and delete the original one
    """
    zipfile = original_file.replace(".txt",".zip")

    with ZipFile(zipfile, 'w') as zipf:
        zipf.write(zipfile, arcname=original_file)
    os.remove(original_file)


def generate_file_name(i):
    """
    :@param: int index i 
    :@return: file name
    """
    if 0<i<10:
        return "corpora/00"+str+".txt"
    elif 10<=i<=100:
        return "corpora/0"+str+".txt"
    elif 100<=i<=1000:
        return "corpora/"+str+".txt"

def main():

    if not os.path.isdir(COPORA_DIR): 
        os.mkdir(COPORA_DIR)    

    if not os.path.exists(CORPUS_0_PATH):
        corpus_0 = analyze.generate_original_corpus(CORPUS_0_FREQ_PATH, CORPUS_0_PATH)
    else:
        with open(CORPUS_0_PATH, "r") as file:
            corpus_0 = file.read(corpus_0)

    corpus_words = analyze.corpus_to_words(corpus_0)
    learned_words = analyze.learn_vocabulary_size(corpus_words)
    _zip(CORPUS_0_PATH)

    print(len(learned_words))

    # chi_dist = {}

    # i = 0
    # for i in range(999):
    #     new_corpus = analyze.sample_w_replacement(corpus_0)
    #     new_corpus_name = generate_file_name(i)

    #     with open(new_corpus_name, "w") as file:
    #         file.writelines(new_corpus)
    #     _zip(new_corpus_name)

    #     corpus_words = analyze.corpus_to_words(new_corpus)
    #     learned_words = analyze.learn_vocabulary_size(corpus_words)

    #     chi_dist[i] = len(learned_words)

    # with open("analysis/dev_child.json","w") as file:
    #     file.dump(chi_dist,file,index=4)

main()










