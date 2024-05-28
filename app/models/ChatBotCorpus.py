import nltk
import string

from nltk import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import unidecode

from flask import Blueprint

bot_bp = Blueprint('bot', __name__)


class Bot:
    def __init__(self, corpus_path):
        self.stemmer = SnowballStemmer('spanish')
        self.load_corpus(corpus_path)
        nltk.download('stopwords')
        nltk.download('punkt')
        nltk.download('wordnet')

    def load_corpus(self, corpus_path):
        with open(corpus_path, 'r', encoding='utf-8', errors='ignore') as f:
            raw = f.read()
        self.raw = raw.lower()
        self.sent_tokens = nltk.sent_tokenize(self.raw)
        self.word_tokens = nltk.word_tokenize(self.raw)

    def LemTokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def LemNormalize(self, text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        normalized_text = self.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
        return [unidecode.unidecode(token) for token in normalized_text]

    def response(self, user_response):
        robo_response = ''
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words=stopwords.words('spanish'))
        tfidf = TfidfVec.fit_transform(self.sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        if req_tfidf == 0:
            robo_response = "Lo siento, no tengo respuesta a tu pregunta."
        else:
            robo_response = self.sent_tokens[idx]
        self.sent_tokens.pop()
        return robo_response