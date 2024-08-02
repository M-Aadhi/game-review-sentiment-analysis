# Game Review Sentiment Analysis

## Objective
Build a model to classify game reviews as positive or negative based on their text.

## Dataset
- The dataset used is from [Kaggle](https://www.kaggle.com/datasets/luthfim/steam-reviews-dataset).

## Project Structure
- `data/`: Contains the dataset.
- `notebooks/`: Contains Jupyter notebooks for data exploration and model building.
- `src/`: Contains scripts for preprocessing, model training, and evaluation.
- `requirements.txt`: Lists the Python dependencies.
- `README.md`: Project documentation.

## Steps
1. **Data Collection:** 
   - Download the dataset from Kaggle.

2. **Data Preprocessing:** 
   - Clean the text data.
   - Tokenize the text.
   - Convert text data into numerical format using TF-IDF.

3. **Exploratory Data Analysis (EDA):**
   - Visualize the distribution of positive and negative reviews.
   - Generate word clouds for positive and negative reviews.

4. **Model Building:**
   - Train a Logistic Regression model.
   - Evaluate the model using accuracy, precision, recall, and F1-score.

5. **Model Evaluation:**
   - Use the testing set to evaluate the performance of your model.
   - Create a confusion matrix to visualize the results.

## Usage
1. Install the required packages:
   ```bash
   pip install -r requirements.txt

## Explanation 
TF-IDF stands for Term Frequency-Inverse Document Frequency. It’s a statistical measure used to evaluate the importance of a word in a document relative to a collection of documents (corpus). Here’s a breakdown:

Term Frequency (TF): Measures how frequently a word appears in a document. It’s calculated as:

TF
(
𝑡
,
𝑑
)
=
Number of times term 
𝑡
 appears in document 
𝑑
Total number of terms in document 
𝑑
TF(t,d)= 
Total number of terms in document d
Number of times term t appears in document d
​
 
Inverse Document Frequency (IDF): Measures how important a term is across the entire corpus. It’s calculated as:

IDF
(
𝑡
,
𝐷
)
=
log
⁡
(
Total number of documents 
∣
𝐷
∣
Number of documents containing term 
𝑡
)
IDF(t,D)=log( 
Number of documents containing term t
Total number of documents ∣D∣
​
 )
TF-IDF Score: Combines both TF and IDF to give a measure of the term’s importance:

TF-IDF
(
𝑡
,
𝑑
,
𝐷
)
=
TF
(
𝑡
,
𝑑
)
×
IDF
(
𝑡
,
𝐷
)
TF-IDF(t,d,D)=TF(t,d)×IDF(t,D)
Usage in Sentiment Analysis:

TF-IDF helps convert text data into numerical features that capture the significance of words relative to the document and corpus. This is useful for machine learning models to understand and classify text data based on the frequency and importance of words.

In this project, TF-IDF was used to convert game reviews into numerical vectors that could be fed into a machine learning model for sentiment classification.
