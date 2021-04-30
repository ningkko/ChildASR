import src.analyze as analyze
import pandas as pd
import numpy as np
from zipfile import ZipFile
import os
import json
import tqdm
import math
import argparse


parser = argparse.ArgumentParser(description='.')
parser.add_argument('--month', type=int, help='Age of the kids')
parser.add_argument('--group', type=str, help='Bilingual (bi) or typical (dev)')

args = parser.parse_args()


month = args.month
# CORPUS_0_PATH = "src/words/dev_utt.txt"
# LEARNING_RATE = 0.1
group = args.group
dev_corpus_path = "corpora/dev_000.txt"
bi_corpus_path = "corpora/bi_000.txt"
# # norwegian
factor = 5.336256180469715
# chinese
# factor = 3.7862052142969884


INITIALIZE_BI = False
if group == "dev":
    CORPUS_0_PATH = dev_corpus_path
    corpus_size = int(analyze.input_voc(month)/factor)

else:
    corpus_size = int(analyze.input_voc(month)/factor/2)
    CORPUS_0_PATH = bi_corpus_path
    if not os.path.exists(bi_corpus_path):
        CORPUS_0_PATH = dev_corpus_path
        INITIALIZE_BI = True

# with open("lr/bi_30.json","r") as file:
#     lr = json.load(file)
with open("lr/dev_"+str(month)+".json","r") as file:
    lr_dict = json.load(file)
    selected_words = [k for k, v in lr_dict.items()]

def zip_freq(original_file_path):
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
    os.chdir("../../")


def generate_file_name(i, group):
    """
    :@param: int index i 
    :@return: file name
    """
    if 0<i<10:
        return "corpora/"+group+"/00"+str(i)+".json"
    elif 10<=i<100:
        return "corpora/"+group+"/0"+str(i)+".json"
    elif 100<=i<1000:
        return "corpora/"+group+"/"+str(i)+".json"

def main(): 

    if not os.path.exists(CORPUS_0_PATH):
        print("Run extract_utterance.py first")
        exit(1)
    else:
        with open(CORPUS_0_PATH, "r") as file:
            corpus_0 = file.read().split("\n")  

    if not os.path.exists("corpora/"+group):
        os.mkdir("corpora/"+group)

    if INITIALIZE_BI:
        corpus_0 = analyze.sample_w_replacement(corpus_0, corpus_size)

        with open(bi_corpus_path,"w") as file:
            file.write("\n".join(corpus_0))

    ## get the freq dict 
    word_freq = analyze.corpus_to_word_freq(corpus_0)
    with open("corpora/"+group+"/000.json", "w") as file:
        json.dump(word_freq,file,indent=4)
    learned_words = analyze.learn_vocabulary_size(word_freq, lr_dict, selected_words)

    # print(len(learned_words))

    chi_dist = {0:len(learned_words)}
    
    # pbar = tqdm.tqdm(total=3)
    pbar = tqdm.tqdm(total=999)

    i = 1
    while i < 1000:
    # while i<3:
        new_corpus_name = generate_file_name(i, group)

        if os.path.exists(new_corpus_name):
            with open(new_corpus_name,"r") as file:
                word_freq = json.load(file)
        else:
            new_corpus = analyze.sample_w_replacement(corpus_0, corpus_size)
            word_freq = analyze.corpus_to_word_freq(new_corpus)

            with open(new_corpus_name, "w") as file:
                json.dump(word_freq,file,indent=4)
            # zip_freq(new_corpus_name)
        
        selected_dict, learned_words = analyze.learn_vocabulary_size(word_freq, lr_dict, selected_words)
        with open(new_corpus_name, "w") as file:
            json.dump(selected_dict,file,indent=4)

        chi_dist[i] = len(learned_words)
        pbar.update(1)
        i += 1

    with open("analysis/"+group+"_child.json","w") as file:
        json.dump(chi_dist,file,indent=4)

main()











