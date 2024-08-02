import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from preprocess import df
# Visualizing sentiment distribution


df = df


sns.countplot(df['recentReviews'])
plt.title('Sentiment Distribution')
plt.show()

# Word clouds (optional)
from wordcloud import WordCloud

df = df.dropna(subset=['recentReviews'])
positive_reviews = ' '.join(df[df['recentReviews'].str.contains('Positive')]['description'])
negative_reviews = ' '.join(df[df['recentReviews'].str.contains('Negative')]['description'])

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
