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
