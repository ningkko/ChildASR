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

        print("On corpus %s"%corpus_name)

        data_dir = corpus_name+"/"
        # print(data_dir)
        if not os.path.isdir(data_dir): 
            os.mkdir(data_dir)

        # if not glob.glob(data_dir+".cha"):

            print("Preparing reference files...")
            files = prep.prep_file(corpus_p) 

        #     print("Downloading...")
        #     shellscript = subprocess.Popen(["src/prep/download.sh"], stdin=subprocess.PIPE)
        #     returncode = shellscript.wait()  # download data

            print("Finding transcripts in %s..."%corpus_p)
            kept_num = delete_files.delete_files(data_dir, files)
            print("%i cha files kept\n==================================="%kept_num)

        all_words = pd.DataFrame()
        word_p = "src/words/"+corpus_name+".csv"
        if os.path.exists(word_p):
            print("word file exists")
            all_words = pd.read_csv(word_p)
            if all_words.empty:
                print("file empty")
    
        if all_words.empty:
            print("extracting words from transcripts..")
            all_words = analyze.get_words(corpus_name)

if __name__ == "__main__":
    main()

           