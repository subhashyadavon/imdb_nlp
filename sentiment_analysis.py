from datasets import load_dataset
import re, html, unicodedata, contractions
import nltk, spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import pickle
import os

# -----------------------------
# 1. Load dataset
# -----------------------------
dataset = load_dataset("imdb")
train_texts = dataset["train"]["text"]
train_labels = dataset["train"]["label"]
test_texts = dataset["test"]["text"]
test_labels = dataset["test"]["label"]

# -----------------------------
# 2. Cleaning and normalization
# -----------------------------
def clean_text(text, expand_contractions=True, remove_html=True):
    if remove_html:
        text = re.sub(r"<.*?>", " ", text)
    text = html.unescape(text)
    if expand_contractions:
        text = contractions.fix(text)
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

# -----------------------------
# 3. Tokenization + stopword removal
# -----------------------------
nltk.download("punkt_tab")
nltk.download("stopwords")
stop = set(stopwords.words("english"))

def tokenize_and_filter(text):
    toks = word_tokenize(text)
    toks = [t for t in toks if t.isalpha() and t not in stop]
    return toks

# -----------------------------
# 4. Lemmatization
# -----------------------------
# Make sure the model is installed:
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm", disable=["parser","ner"])

def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([tok.lemma_ for tok in doc if tok.is_alpha and not tok.is_stop])

# -----------------------------
# 5. Preprocess whole dataset
# -----------------------------
def preprocess(text):
    text = clean_text(text)
    text = " ".join(tokenize_and_filter(text))
    text = lemmatize_text(text)
    return text

print("Preprocessing train data (25k reviews)...")
train_clean = [preprocess(t) for t in train_texts]
train_y = train_labels

print("Preprocessing test data (25k reviews)...")
test_clean = [preprocess(t) for t in test_texts]
test_y = test_labels

# -----------------------------
# 6. Vectorization (TF-IDF)
# -----------------------------
vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
X_train = vectorizer.fit_transform(train_clean)
X_test = vectorizer.transform(test_clean)

# -----------------------------
# 7. Train model (Logistic Regression)
# -----------------------------
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, train_y)

# -----------------------------
# 8. Evaluate model
# -----------------------------
preds = clf.predict(X_test)
print("Accuracy:", accuracy_score(test_y, preds))
print(classification_report(test_y, preds))



# create 'model' folder if it doesn't exist
if not os.path.exists("model"):
    os.makedirs("model")


# Save TF-IDF vectorizer
with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save Logistic Regression model
with open("model/clf.pkl", "wb") as f:
    pickle.dump(clf, f)


