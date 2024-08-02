import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from preprocess import df  # Ensure df is correctly imported from preprocess.py
from wordcloud import WordCloud

# Enable interactive mode
plt.ion()

print(f"Shape of the dataframe: {df.shape}")

# Check for missing values
print("Missing values in each column:\n", df.isnull().sum())

# Basic statistics
print("Basic statistics:\n", df.describe())

# Check column names and data types
print("Column names and data types:\n", df.dtypes)

# Check for duplicate rows
print("Number of duplicate rows:", df.duplicated().sum())
# Visualizing sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='sentiment', data=df)
plt.title('Sentiment Distribution')

# Ensure df is correctly loaded
df = df.dropna(subset=['recentReviews'])

# Visualizing sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='recentReviews', data=df)
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()


# Generate word clouds
positive_reviews = ' '.join(df[df['recentReviews'].str.contains('Positive', case=False, na=False)]['description'])
negative_reviews = ' '.join(df[df['recentReviews'].str.contains('Negative', case=False, na=False)]['description'])

positive_wordcloud = WordCloud(width=800, height=400, background_color='white').generate(positive_reviews)
negative_wordcloud = WordCloud(width=800, height=400, background_color='black').generate(negative_reviews)

plt.figure(figsize=(10, 5))
plt.imshow(positive_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Positive Reviews Word Cloud')
plt.show()

plt.figure(figsize=(10, 5))
plt.imshow(negative_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Negative Reviews Word Cloud')
plt.show()
