import os
import glob
import pickle
import ast 
import subprocess
import json
import glob
import pandas as pd

import src.prep.prep as prep
import src.prep.delete_files as delete_files
import src.analyze as analyze

with open("config.json","r") as file:
    config = json.load(file)
    corpora_paths = ast.literal_eval(config["corpora_paths"])


def main():

    for corpus_p in corpora_paths: 

        corpus_name = corpus_p.split(".")[0]

        all_utts = pd.DataFrame()
        utt_p = "src/words/"+corpus_name+"utt_freq.csv"
        if os.path.exists(utt_p):
            print("utterance file exists")
            all_utts = pd.read_csv(utt_p)
            if all_utts.empty:
                print("file empty")
    
        if all_utts.empty:
            print("extracting utterances from transcripts..")
            all_utts = analyze.get_utterance(corpus_name)

if __name__ == "__main__":
    main()

           