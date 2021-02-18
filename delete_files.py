import pickle

file = open("files.pkl",'rb')
no_remove = pickle.load(file)

i = 0
import os
for f in os.listdir('data/.'):
    if os.path.isdir(f):
        os.rmdir(f)

    elif f not in no_remove:
        print('unlink:' + f ) 
        os.remove(f)

    else:
        i+=1

print("%i cha files kept"%i)
