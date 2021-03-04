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

        all_utts = []
        utt_p = "src/words/"+corpus_name+"_utt.txt"
        if os.path.exists(utt_p):
            print("utterance file exists")
            with open(utt_p,"r") as file:
               all_utts = file.read()
            if not all_utts:
                print("file empty")
    
        # if all_utts.empty:
        #     print("extracting utterances from transcripts..")
        #     all_utts = analyze.get_utterance(corpus_name)
        all_utts = analyze.get_utterances_from_cha(corpus_name)


if __name__ == "__main__":
    main()

           