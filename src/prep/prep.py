import pandas as pd
import pickle
import argparse
import os

def _find_cha_path(x):
    """
    returns a cha file path from the path column entries in the xls files
    """
    return 'data/'+"/".join(x.split("/")[1:])+'.cha'

def _find_website(x):
        xs = x.split("/")
        newx = xs[1:3]
        return "https://childes.talkbank.org/data/"+"/".join(newx)+".zip"

def prep_file(x):
    """
    This file creates reference files for downloading and preparing the copora
    :param x: the file path to xls file 
    :return: 1. writes a list of websites that contains downloading links to the copora;
             2. a list of files as a reference of files to keep 
    """
    # print(args.input_path)
    df = pd.read_excel(x, names=["path", "1", "2", "3", "4", "5","6","7","8"])

    df["website"] = df["path"].apply(lambda x: _find_website(x))
    websites = df["website"].unique()

    with open("websites.txt","w") as file:
        file.write("\n".join(websites))
    
    df["files"] = df["path"].apply(lambda x: _find_cha_path(x))
    files = set(df['files'].unique())

    filehandler = open(b"files.pkl","wb")
    pickle.dump(files,filehandler)

    return files


