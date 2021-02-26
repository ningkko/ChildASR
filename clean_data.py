import os
import glob
import pickle
import ast 
import subprocess
import json
import glob

with open("config.json","r") as file:
    config = json.load(file)
    corpora_paths = ast.literal_eval(config["corpora_paths"])

import sys
import src.analyze as analyze
import src.prep.prep as prep
import src.prep.delete_files as delete_files


def main():

    for corpus_p in corpora_paths: 

        corpus_name = corpus_p.split(".")[0]

        print("Finding transcripts in %s..."%corpus_p)
        
        # filehandler = open(b"files.pkl","rb")
        # files = pickle.load(filehandler)
        files = prep.prep_file(corpus_p) 
        kept_num = delete_files.delete_files(corpus_p, files)

        print("%i cha files kept\n==================================="%kept_num)

        all_words = []
        word_p = "src/words/"+corpus_name+".pkl"
        if os.path.exists(word_p):
            print("word file exists")
            with open(word_p, 'rb') as f:
                try:
                    all_words = pickle.load(f)
                except IOError:
                    print("file empty")
                    
        if not all_words:
            print("extracting words from transcripts..")
            all_words = analyze.get_words(corpus_name)

        print("analyzing...")
        analyze.plot(corpus_name, all_words)


if __name__ == "__main__":
    main()