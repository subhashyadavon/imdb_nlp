from flask import Flask, render_template, request
import pickle
import re, html, unicodedata, contractions
import nltk, spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# -----------------------------
# 1. Load trained model
# -----------------------------
with open("model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("model/clf.pkl", "rb") as f:
    clf = pickle.load(f)

# -----------------------------
# 2. Preprocessing tools
# -----------------------------
nltk.download("punkt")
nltk.download("stopwords")
stop = set(stopwords.words("english"))

nlp = spacy.load("en_core_web_sm", disable=["parser","ner"])

def clean_text(text, expand_contractions=True, remove_html=True):
    if remove_html:
        text = re.sub(r"<.*?>", " ", text)
    text = html.unescape(text)
    if expand_contractions:
        text = contractions.fix(text)
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

def tokenize_and_filter(text):
    toks = word_tokenize(text)
    return [t for t in toks if t.isalpha() and t not in stop]

def lemmatize_text(text):
    doc = nlp(text)
    return " ".join([tok.lemma_ for tok in doc if tok.is_alpha and not tok.is_stop])

def preprocess(text):
    text = clean_text(text)
    text = " ".join(tokenize_and_filter(text))
    text = lemmatize_text(text)
    return text

# -----------------------------
# 3. Flask app
# -----------------------------
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = ""
    review = ""
    if request.method == "POST":
        review = request.form["review"]
        clean_review = preprocess(review)
        vect_review = vectorizer.transform([clean_review])
        pred = clf.predict(vect_review)[0]
        sentiment = "Positive" if pred == 1 else "Negative"
    return render_template("index.html", sentiment=sentiment, review=review)

if __name__ == "__main__":
    app.run(debug=True)
