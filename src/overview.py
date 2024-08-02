import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from preprocess import df

# Load the trained model
model = joblib.load('model.pkl')

# Load the vectorizer
vectorizer = joblib.load('vectorizer.pkl')

# Vectorize the text data using the loaded vectorizer
X = vectorizer.transform(df['cleaned_review'])

# Predict using the loaded model
predictions = model.predict(X)
df['predictions'] = predictions

# Save predictions to a file
df.to_csv('../data/predicted_steam_data.csv', index=False)