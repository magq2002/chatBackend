import torch
from transformers import BertTokenizer, BertForSequenceClassification
import json
import nltk
import string
import unidecode
from nltk.corpus import stopwords

from flask import Blueprint

botBert_bp = Blueprint('botBert', __name__)


class BotBert:
    def __init__(self, model_path, corpus_path):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.stop_words = set(stopwords.words('spanish'))
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_corpus(corpus_path)

    def clean_text(self, text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        normalized_text = nltk.word_tokenize(text.lower().translate(remove_punct_dict))
        normalized_text = [unidecode.unidecode(token) for token in normalized_text if token not in self.stop_words]
        return " ".join(normalized_text)

    def load_corpus(self, corpus_path):
        with open(corpus_path, 'r', encoding='utf-8') as f:
            self.corpus = json.load(f)

    def response(self, user_response):
        clean_user_response = self.clean_text(user_response)
        inputs = self.tokenizer(clean_user_response, return_tensors="pt", padding=True, truncation=True).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_label_idx = torch.argmax(logits, dim=1).item()

        response = self.corpus.get(str(predicted_label_idx), "Lo siento, no tengo respuesta a tu pregunta.")
        return response