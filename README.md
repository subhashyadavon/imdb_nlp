# IMDB Sentiment Analysis Web App

This repository contains a **web application** that demonstrates a **movie review sentiment classifier** built using **TF-IDF and Logistic Regression**. Users can type in an IMDB movie review and see whether the sentiment is **Positive** or **Negative**.  

The project also showcases **NLP concepts and preprocessing techniques** used in real-world text classification tasks.

---

## **Demo**

- Enter a movie review in the text box.  
- Preprocesses the review (cleaning, tokenization, lemmatization).  
- Predicts sentiment using the trained model.  
- Displays the result interactively.

---
## **How to Run the App**

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/subhashyadavon/imdb_nlp.git
cd imdb_nlp
```

### 2. Create a Virtual Environment
```bash
python3 -m venv sentiment-analysis
```
### 3. Activate the Virtual Environment
```bash
# On macOS/Linux
source sentiment-analysis/bin/activate
# On Windows
sentiment-analysis\Scripts\activate
```
### 4. Install Dependencies
```bash
python3 sentiment_analysis.py
```

### 5. Run the flask app
```bash
python3 app.py
```






