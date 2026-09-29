import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load the cleaned dataset
print("Loading cleaned dataset...")
df = pd.read_csv("books_data_clean.csv")

# Combine 'title' and 'description' for maximum text context
df['combined_text'] = df['title'] + " " + df['description']

# Predict the 'category' based on the combined text
X_text = df['combined_text']  # Input feature
y_target = df['category']   # Target label (the category)