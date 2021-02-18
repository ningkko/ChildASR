import pickle

file = open("files.pkl",'rb')
no_remove = pickle.load(file)

import os
import shutil

i = 0

for root, dirs, files in os.walk('childes/'):
	if not dirs:
		for file in files:
			file_path = root+"/"+file
			if file_path in no_remove:
				ff = shutil.move(file_path, "data/")
				file_path = file_path.replace("/","_")
				os.rename(ff,file_path)
				i+=1

print("%i cha files kept"%i)
