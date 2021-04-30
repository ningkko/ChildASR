import os
import glob
import pickle
import ast 
import subprocess
import json
import glob
import pandas as pd
import argparse

import src.prep.prep as prep
import src.prep.delete_files as delete_files
import src.analyze as analyze

with open("config.json","r") as file:
    config = json.load(file)
    corpora_paths = ast.literal_eval(config["corpora_paths"])

parser = argparse.ArgumentParser(description='.')
parser.add_argument('--lang', type=str, help='eng, nor, chi, ita')

args = parser.parse_args()
lang =args.lang


def main():

    for corpus_p in corpora_paths: 

        corpus_name = corpus_p.split(".")[0]

        # all_utts = []
        # utt_p = "corpora/dev_000.txt"
        # if os.path.exists(utt_p):
        #     print("utterance file exists")
        #     with open(utt_p,"r") as file:
        #        all_utts = file.read()
        #     if not all_utts:
        #         print("file empty")
    
        # if all_utts.empty:
        #     print("extracting utterances from transcripts..")
        #     all_utts = analyze.get_utterance(corpus_name)
        analyze.get_utterances_from_cha(corpus_name, lang)


if __name__ == "__main__":
    main()

           