# ChildASR
Work done for L3@BC


Lit review: https://public.3.basecamp.com/p/9v7jBAYbvW9amJC594Y5sXAn

To download transcripts from childesDB (stored in data/):

1. pre-select transcripts from https://talkbank.org/DB/
2. download the xls file and store to the current path (root/)
3. run the following command to extract all unique corpora downloading links in the xls file
```
python3 prep.py
```
This should create a website.txt file
4. run the following command to download all corpora in website.txt and recursively unzip all zip files to extract CHAT transcripts (zip files will be deleted after unzipping).
```
sh download.sh
```
