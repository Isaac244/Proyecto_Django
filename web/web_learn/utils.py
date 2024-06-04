import os
import pickle
import re
import nltk
import string
nltk.download('stopwords')
nltk.download('punkt')
import pandas as pd

from nltk.corpus import stopwords
from django.conf import settings
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity

#product_vectorizer = pickle.load(open(os.path.join(settings.BASE_DIR, "./web_learn/data/product_vectorizer.pickle"), "rb"))
product_matriz = pickle.load(open(os.path.join(settings.BASE_DIR, "./web_learn/data/product_matriz.pickle"), "rb"))
system_recomend = pickle.load(open(os.path.join(settings.BASE_DIR, "./web_learn/data/productos_nombre.pickle"), "rb"))

def normalize(raw):
    letras = re.sub("[^a-zA-Z]$"," ", raw)
    minusculas = letras.lower()
    stop_free = " ".join([i for i in minusculas.split() if i not in set(stopwords.words('english'))])
    punc_free = "".join(ch for ch in stop_free if ch not in set(string.punctuation))
    word_tokens = word_tokenize(punc_free)
    filtered_sentence = [(WordNetLemmatizer().lemmatize(w, "v")) for w in word_tokens]
    return filtered_sentence

cosine_sim = cosine_similarity(product_matriz, product_matriz)

real_df = system_recomend.reset_index()
titles = real_df['product_name']
indices = pd.Series(real_df.index, index=real_df['product_name'])

def recomender(product_name):
    idx = indices[product_name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    product_indices = [i[0] for i in sim_scores]
    return titles.iloc[product_indices]