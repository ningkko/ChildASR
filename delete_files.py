import pickle

file = open("files.pkl",'rb')
no_remove = pickle.load(file)

i = 0
import os
import shutil

for f in os.listdir('data/.'):
    if os.path.isdir('data/'+f):
        shutil.rmtree('data/'+f)

    elif f not in no_remove:
        print('unlink:' + f ) 
        os.remove('data/'+f)

    else:
        i+=1

print("%i cha files kept"%i)
