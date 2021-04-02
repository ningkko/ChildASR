# Bilingual
Tries to find out the reason for bilingual children not performing as well as monolingual children in English fluency tests.

>> Work done at L3@BC
Log: https://docs.google.com/document/d/1BI81WpWN63e13zJxiNQWVubdNLdnJaHqt6ESZx9AMEI/edit?usp=sharing

## How to run
1. pre-select transcripts from https://talkbank.org/DB/
The .xls file downloaded from talkbank cannot be opened by pandas directly. Make sure to open (maybe in excel) and resave it as a .xls file.
2. download the xls file and store it to the current path (root/)
3. Specify paths to xls files in config.json
4. run the following file

```
python3 fetch_data.py
python3 extract_utternace.py
python3 simulate.py --month [month of the kids, 30 used] --group [bi or dev]
python3 plot.py
```

## The CHAT format manual
https://talkbank.org/manuals/CHAT.pdf

## Methods of checking if a word is English:
1. clk3 didn't work well (in general)
2. enchant didn't work well (can't distinguish Mandarin and English and punctuations)
3. nltk words (used in the current version): a dictionary of len(words.words())) -> 235892 English words. Should suffice


## Previous lit review: https://public.3.basecamp.com/p/9v7jBAYbvW9amJC594Y5sXAn