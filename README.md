# Bilingual
Tries to find out the reason for bilingual children not performing as well as monolingual children in English fluency tests.

>> Work done at L3@BC

## How to run
1. pre-select transcripts from https://talkbank.org/DB/
2. download the xls file and store it to the current path (root/)
3. Specify paths to xls files in config.json
4. run the following file

```
python3 setup.py
```

## The CHAT format manual
https://talkbank.org/manuals/CHAT.pdf

## Methods of checking if a word is English:
1. clk3 didn't work well (in general)
2. enchant didn't work well (can't distinguish Mandarin and English and punctuations)
3. nltk words (used in the current version): a dictionary of len(words.words())) -> 235892 English words. Should suffice


## Previous lit review: https://public.3.basecamp.com/p/9v7jBAYbvW9amJC594Y5sXAn