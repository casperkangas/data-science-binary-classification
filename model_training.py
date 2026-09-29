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

print("Converting text into mathematical features (TF-IDF)...")

# Initialize the vectorizer. max_features=1000 keeps only the top 1000 most meaningful words and stop_words='english' removes useless filler words
vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')

# 'fit_transform' analyzes the vocabulary and turns the text into a math matrix
X_features = vectorizer.fit_transform(X_text)

print("Splitting data into Training and Testing sets...")
# Hide 20% of the data to give the model a "fair test" later and random_state=42 is just a seed that ensures the exact same split every run
X_train, X_test, y_train, y_test = train_test_split(X_features, y_target, test_size=0.2, random_state=42)

print("Training the Logistic Regression model...")

# Initialize the model
model = LogisticRegression()

# The .fit() command is where the actual "learning" happens, with feeding it the training keywords (X_train) and the correct answers (y_train)
model.fit(X_train, y_train)