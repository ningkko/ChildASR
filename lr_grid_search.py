#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !ls "./"


# In[2]:


# !pip3 install nltk
# !pip3 install pattern
# !pip3 install tdqm
# !pip3 install --upgrade ipykernel
# !pip3 install seaborn
# !pip3 install nltk


# In[3]:


# import json
# with open("analysis/bi_child.json","r") as file:
#     bi_child = json.load(file)
# with open("analysis/dev_child.json","r") as file:
#     dev_child = json.load(file)


# In[4]:


# import src.analyze as analyze
# analyze.plot(dev_child, bi_child)


# In[4]:


with open("corpora/000_bi.txt") as file:
    bi = file.read().split("\n")
    bi_text = []
    for sentence in bi:
        words = sentence.split(" ")
        if words:
            bi_text+=words
    
with open("corpora/000_dev.txt") as file:
    dev = file.read().split("\n")
    dev_text = []
    for sentence in dev:
        words = sentence.split(" ")
        if words:
            dev_text+=words


# In[5]:


import nltk
from nltk.probability import FreqDist




import numpy as np

lambdas = np.arange(0.0005, 0.025, 0.001).tolist()
input_word_ranges = np.arange(20000, len(dev)+1, 40000).tolist()
k = 10



n_words = []
learning_rates = []
n_learned_words = []


# In[64]:


import random
from scipy.stats import binom

def get_n_learned_words(learning_rate, input_word_range, corpus):
    words = random.sample(corpus, input_word_range)
    freq = nltk.FreqDist(words)
    freq.pop("",None)
    # freq.plot(25, cumulative=False)
    learned = []
    for k,v in freq.items():
        prob = 1-binom.cdf(0, v, learning_rate)
        indicator = random.random()
        if indicator < prob:
            learned.append(k)
    # print("%f, %i"%(learning_rate,len(learned)))
    return len(learned)


# In[65]:


# from scipy.stats import poisson
# def cdf(word_freq, n_total_words, learning_rate):
#     return poisson.cdf(word_freq/n_total_words, learning_rate)
# poisson.cdf(0,0.1)

# In[66]:


import tqdm
pbar = tqdm.tqdm(total=len(lambdas)*len(input_word_ranges))
for lmda in lambdas:
    for input_word_range in input_word_ranges:
        n_words.append(input_word_range)
        learning_rates.append(lmda)
#         print(lmda)
        n_learned_words.append(get_n_learned_words(lmda, input_word_range, corpus=dev))
        pbar.update(1)


# In[ ]:


import pandas as pd
df = pd.DataFrame(list(zip(n_words, learning_rates,n_learned_words)), 
                           columns =['#input_word', 'learning_rate','#learned_word'])
df = df[df["learning_rate"]<=3]
df


# In[ ]:


df.to_csv('analysis/dev.csv')


# In[ ]:


df=df.pivot("#input_word","learning_rate","#learned_word")
df


# In[ ]:


import seaborn as sns
p = sns.lineplot(data=df)
p.figure.savefig("analysis/dev.jpeg",dpi=100)


# In[ ]:


n_words_bi = []
learning_rates_bi = []
n_learned_words_bi = []
pbar = tqdm.tqdm(total=len(lambdas)*len(input_word_ranges))
for lmda in lambdas:
    for input_word_range in input_word_ranges:
        n_words_bi.append(input_word_range)
        learning_rates_bi.append(lmda)
        n_learned_words_bi.append(get_n_learned_words(lmda, input_word_range, corpus=bi))
        pbar.update(1)


# In[ ]:


df2 = pd.DataFrame(list(zip(n_words_bi, learning_rates_bi,n_learned_words_bi)), 
                           columns =['#input_word', 'learning_rate','#learned_word'])
# df2 = df2[df2["learning_rate"]<=3]
# df2


# In[ ]:


df2.to_csv('analysis/bi.csv',index=False)


# In[ ]:


df2=df2.pivot("#input_word","learning_rate","#learned_word")
# df2


# In[ ]:


p2 = sns.lineplot(data=df2)
p2.figure.savefig("analysis/bi.jpeg",dpi=100)


# In[ ]:




