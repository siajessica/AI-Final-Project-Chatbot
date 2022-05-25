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

raw_corpus = json.loads(open('covid_info.txt', 'r').read())
rm_punctuation(raw_corpus)
sentences = nltk.sent_tokenize(raw_corpus)
words = nltk.word_tokenize(raw_corpus)
lemma = nltk.stem.WordNetLemmatizer()

def perform_lemmatization(tokens):
    return [lemma.lemmatize(token) for token in tokens]
  
 remove_punctuation = dict((ord(punc), None) for punc in string.punctuation)
  
 def processed_data(document):
    return perform_lemmatization(nltk.word_tokenize(document.lower().translate(remove_punctuation)))
  
 def generate_answers(str):
    if punc_remove(str.lower()) in question_answers:
        return question_answers[punc_remove(str.lower())]

def generate_response(user):
    bracrobo_response = ''
    sentences.append(user)

    word_vectorizer = TfidfVectorizer(tokenizer=processed_data, stop_words='english')
    all_word_vectors = word_vectorizer.fit_transform(sentences)
    similar_vector_values = cosine_similarity(all_word_vectors[-1], all_word_vectors)
    similar_sentence_number = similar_vector_values.argsort()[0][-2]

    matched_vector = similar_vector_values.flatten()
    matched_vector.sort()
    vector_matched = matched_vector[-2]

    if vector_matched is 0:
        bracrobo_response = bracrobo_response + 'Sorry, my database doesn\'t have the response for that. Try ' \
                                                'something different and related to Brac. '
        return bracrobo_response
    else:
        bracrobo_response = bracrobo_response + sentences[similar_sentence_number]
        return bracrobo_response
      

flag = True
print("Hi! I am Sarcov. Ask me any questions about COVID-19 in Taiwan: ")
while flag:
  user_input = input().lower()
  user_input = rm_punctuation(user_input)
  if user_input != 'bye':
    if user_input in greeting_input:
      print('Sarcov: ' + random.choice(greeting_responses))
    elif generate_answers(user_input) is not None:
                print('BracRobo: ' + generate_answers(user_input))
    else:
      print('haha')
  else:
    flag = False
    print('Sarcov: Bye, take care, remember to wear a mask and stay safe!')
