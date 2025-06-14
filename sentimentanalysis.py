# -*- coding: utf-8 -*-
"""SentimentAnalysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eLRMGi7Moe_9RNhnSA8eOC2bq7z_9ASq
"""

# 1. Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
'''
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('movie_reviews')
from nltk.corpus import movie_reviews
import random
'''

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('movie_reviews')
# Download the specific resource requested by the error
nltk.download('punkt_tab')
from nltk.corpus import movie_reviews
import random

# 2. Load dataset (movie reviews from NLTK)
documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)

data = pd.DataFrame(documents, columns=['words', 'label'])
data['text'] = data['words'].apply(lambda x: ' '.join(x))
data.drop('words', axis=1, inplace=True)

print(data.head())

# 3. Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

# Apply preprocessing
data['clean_text'] = data['text'].apply(preprocess_text)

# 4. Vectorize the text data
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data['clean_text'])

# Encode the labels
le = LabelEncoder()
y = le.fit_transform(data['label'])  # pos = 1, neg = 0

# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# 7. Evaluate the model
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=le.classes_))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# 8. Test with your own sentence
def predict_sentiment(text):
    clean = preprocess_text(text)
    vector = vectorizer.transform([clean])
    pred = model.predict(vector)
    return le.inverse_transform(pred)[0]

# Example
predict_sentiment("I really loved the movie! It was fantastic.")
expressMood = input("Enter your feels: ")# like this : "I really loved the movie! It was fantastic."
predict_sentiment(expressMood )

