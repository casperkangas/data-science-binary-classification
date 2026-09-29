import pandas as pd
import datetime
import argparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Command-line argument parsing, which allows the user to run: python model_training.py --model RF --features 150
parser = argparse.ArgumentParser(description="Train a book classification model.")
parser.add_argument('--model', type=str, choices=['LR', 'RF', 'ALL'], default='LR', help="Choose LR (Logistic Regression), RF (Random Forest), or ALL")
parser.add_argument('--features', type=int, default=100, help="Max number of words for TF-IDF to track")
args = parser.parse_args()

# Load the cleaned dataset
print("Loading cleaned dataset...")
df = pd.read_csv("books_data_clean.csv")

# Combine 'title' and 'description' for maximum text context, with fillna("") to handle any missing values
df['combined_text'] = df['title'].fillna("") + " " + df['description'].fillna("")

# Predict the 'category' based on the combined text
X_text = df['combined_text']  # Input feature
y_target = df['category']   # Target label (the category)

print("Converting text into mathematical features (TF-IDF)...")

# Initialize the vectorizer. max_features=x keeps only the top x most meaningful words and stop_words='english' removes useless filler words
vectorizer = TfidfVectorizer(max_features=args.features, stop_words='english')

# 'fit_transform' analyzes the vocabulary and turns the text into a math matrix
X_features = vectorizer.fit_transform(X_text)

print("Splitting data into Training and Testing sets...")
# Hide 20% of the data to give the model a "fair test" later and random_state=42 is just a seed that ensures the exact same split every run
X_train, X_test, y_train, y_test = train_test_split(X_features, y_target, test_size=0.2, random_state=42)

models_to_test = {}
if args.model in ['LR', 'ALL']:
    models_to_test['Logistic Regression'] = LogisticRegression()
# TODO: Add Random Forest model

for model_name, model in models_to_test.items():
    print(f"\n--- Training {model_name} ---")

    # The .fit() command is where the actual "learning" happens, with feeding it the training keywords (X_train) and the correct answers (y_train)
    model.fit(X_train, y_train)

    print("Evaluating the model's performance...")

    # Ask the trained model to guess the categories for the 20% of data hidden earlier
    y_predictions = model.predict(X_test)

    # Calculate the accuracy (what percentage of its guesses exactly matched y_test)
    accuracy = accuracy_score(y_test, y_predictions)
    print(f"\n*** Final {model_name} Accuracy: {accuracy * 100:.2f}% ***\n")

    # Print a detailed report (shows precision and recall for both Fiction and Nonfiction)
    print(f"Detailed Classification Report: {model_name}")
    print(classification_report(y_test, y_predictions))

    # Append the results to the log file EXPERIMENTS.md
    with open("EXPERIMENTS.md", "a") as f:
            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            inputs_used = f"Title + Description (TF-IDF max {args.features})"
            f.write(f"| {date_str} | {inputs_used} | {model_name} | {accuracy * 100:.2f}% |\n")
    print(f"Results logged to EXPERIMENTS.md!")