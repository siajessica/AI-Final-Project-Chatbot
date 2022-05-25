import pandas as pd
import matplotlib.pyplot as plt
import io
import unicodedata
import random
import numpy as np
import re
import string
import json

#NLP packets
import wordcloud

import nltk
from nltk.corpus import wordnet
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger') 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#stop crashing midway
import warnings
warnings.filterwarnings('ignore')

def rm_punctuation(str):
  punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
  new_str = ''
  for x in str:
    if x not in punctuations:
      new_str = new_str + x
  return new_str

greeting_input = json.loads(open('greetings_start.txt', 'r').read())
greeting_responses = json.loads(open('greetings_responses.txt', 'r').read())

flag = True
print("Hi! I am Sarcov. Ask me any questions about COVID-19 in Taiwan: ")
while flag:
  user_input = input().lower()
  user_input = rm_punctuation(user_input)
  if user_input != 'bye':
    if user_input in greeting_input:
      print('Sarcov: ' + random.choice(greeting_responses))
  else:
    flag = False
    print('Sarcov: Bye, take care, remember to wear a mask and stay safe!')
