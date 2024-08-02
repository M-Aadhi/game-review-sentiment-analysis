import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

import os
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# Load dataset
file_path = r'../data/steam_data.csv'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")
df = pd.read_csv(file_path)

# Check if 'recentReviews' column exists
if 'recentReviews' not in df.columns:
    raise KeyError("The 'recentReviews' column is missing from the dataset.")

# Map review sentiments to numerical values
sentiment_mapping = {
    'Overwhelmingly Positive': 2,
    'Very Positive': 2,
    'Positive': 1,
    'Mostly Positive': 1,
    'Mixed': 0,
    'Mostly Negative': -1,
    'Negative': -2,
    'Very Negative': -2,
    'Overwhelmingly Negative': -2
}
df['sentiment'] = df['recentReviews'].map(sentiment_mapping)

# Cleaning text data
def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

df['cleaned_review'] = df['recentReviews'].apply(clean_text)



df['description'] = df['description'].astype(str)
df['sentiment'] = df['sentiment'].astype(str)
# Check the shape of the dataframe
# Check data types
print(df['sentiment'].dtype)

# Check unique values in the sentiment column
print(df['sentiment'].unique())


