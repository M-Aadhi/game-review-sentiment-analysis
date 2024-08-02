import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from preprocess import df

# Drop rows with NaN values in the 'sentiment' column
df = df.dropna(subset=['sentiment'])

# Print the DataFrame shape after dropping NaNs
print("Shape of DataFrame after dropping NaNs:", df.shape)

# Check the data types
print("Data types in DataFrame:")
print(df.dtypes)

# Check unique values in the sentiment column
print("Unique values in sentiment column:")
print(df['sentiment'].unique())

# Map numerical sentiment values to binary values
def map_sentiment(val):
    try:
        if float(val) in [2.0, 1.0]:
            return 1
        elif float(val) in [0.0, -1.0]:
            return 0
    except ValueError:
        return np.nan

# Apply the mapping
df['sentiment'] = df['sentiment'].apply(map_sentiment)

# Drop any rows with NaN values that might still exist
df = df.dropna(subset=['sentiment'])

# Print the DataFrame shape after mapping
print("Shape of DataFrame after mapping and dropping NaNs:", df.shape)

# Check the distribution of classes
print("Class distribution before train-test split:")
print(df['sentiment'].value_counts())

X = df['cleaned_review']
y = df['sentiment']

# Ensure there are rows available for training and testing
print("Number of samples in X:", len(X))
print("Number of samples in y:", len(y))

if len(X) == 0 or len(y) == 0:
    print("Error: No data available after processing.")
else:
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Check the distribution in training data
    print("Class distribution in y_train:")
    print(y_train.value_counts())

    # Vectorizing text
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Saving the vectorizer
    joblib.dump(vectorizer, 'vectorizer.pkl')

    # Training the model
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)

    # Evaluating the model
    y_pred = model.predict(X_test_vec)
    print(classification_report(y_test, y_pred))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()

    # Saving the model
    joblib.dump(model, 'model.pkl')
