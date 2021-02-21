import pickle
import argparse

# file = open("files.pkl",'rb')
# no_remove = pickle.load(file)

# parser = argparse.ArgumentParser(description='preprocessing the data')
# parser.add_argument('--input_path', type=str,
#                     help='The path to xls file')
# args = parser.parse_args()

import os
import shutil

def delete_files(input_path, no_remove):
    """
    :param input_path: path to the xls file 
    :param keep_list: reference list of files to be kept
    :return numbers of .cha filse kept
    """
    i = 0

    for root, dirs, files in os.walk('data/'):
        if not dirs:
            for file in files:
                file_path = root+"/"+file
                if file_path in keep_list:
                    ff = shutil.move(file_path, args.input_path.split(".")[0]+"/")
                    file_path = file_path.replace("/","_")
                    os.rename(ff,file_path)

                    shutil.move(file_path, args.input_path.split(".")[0]+"/")                
                    i+=1

    return i
