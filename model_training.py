import pandas as pd
import datetime
import argparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline

# Command-line argument parsing, which allows the user to run: python model_training.py --model RF --features 150
parser = argparse.ArgumentParser(description="Train a book classification model.")
parser.add_argument('--model', type=str, choices=['LR', 'RF', 'MLP', 'SVM', 'NB', 'ALL'], default='LR', help="Choose LR (Logistic Regression), RF (Random Forest), MLP (Multi-Layer Perceptron), SVM (Support Vector Machine), NB (Naive Bayes), or ALL")
parser.add_argument('--features', type=int, default=100, help="Maximum number of TF-IDF terms to track")
parser.add_argument('--lr-c', type=float, default=1.0, help="Regularization strength for Logistic Regression (smaller values mean stronger regularization)")
parser.add_argument('--nb-alpha', type=float, default=1.0, help="Additive smoothing strength for Naive Bayes")
parser.add_argument('--analyzer', choices=['word', 'char_wb'], default='word', help="Use word features or character n-grams within word boundaries")
parser.add_argument('--ngram-min', type=int, help="Minimum n-gram size (defaults to 1 for words or 3 for characters)")
parser.add_argument('--ngram-max', type=int, help="Maximum n-gram size (defaults to 1 for words or 5 for characters)")
args = parser.parse_args()

default_ngram_min, default_ngram_max = (1, 1) if args.analyzer == 'word' else (3, 5)
if args.ngram_min is None and args.ngram_max is None:
    args.ngram_min, args.ngram_max = default_ngram_min, default_ngram_max
else:
    if args.ngram_min is None:
        args.ngram_min = default_ngram_min
    if args.ngram_max is None:
        args.ngram_max = max(default_ngram_max, args.ngram_min)

if args.features < 1:
    parser.error("--features must be at least 1")
if args.lr_c <= 0:
    parser.error("--lr-c must be greater than 0")
if args.nb_alpha <= 0:
    parser.error("--nb-alpha must be greater than 0")
if args.ngram_min < 1 or args.ngram_max < 1:
    parser.error("--ngram-min and --ngram-max must be at least 1")
if args.ngram_min > args.ngram_max:
    parser.error("--ngram-min cannot be greater than --ngram-max")

# Load the cleaned dataset
print("Loading cleaned dataset...")
df = pd.read_csv("books_data_clean.csv")

# Combine 'title' and 'description' for maximum text context, with fillna("") to handle any missing values
df['combined_text'] = df['title'].fillna("") + " " + df['description'].fillna("")

# Predict the 'category' based on the combined text
X_text = df['combined_text']  # Input feature
y_target = df['category']   # Target label (the category)

print("Converting text into mathematical features (TF-IDF)...")
stop_words = 'english' if args.analyzer == 'word' else None
print(
    f"TF-IDF settings: analyzer={args.analyzer}, max_features={args.features}, "
    f"n-grams={args.ngram_min}-{args.ngram_max}, "
    f"stop_words={'english' if stop_words else 'none'}"
)
print("Evaluation: stratified 80/20 holdout (random_state=42)")

# Initialize the vectorizer, while the pipeline fits it only on the training split
# max_features limits the number of terms and analyzer selects words or character n-grams
vectorizer = TfidfVectorizer(
    max_features=args.features,
    analyzer=args.analyzer,
    stop_words=stop_words,
    ngram_range=(args.ngram_min, args.ngram_max),
)

# Use one reproducible, stratified 80/20 split for a single set of test metrics
X_train, X_test, y_train, y_test = train_test_split(
    X_text,
    y_target,
    test_size=0.2,
    random_state=42,
    stratify=y_target,
)

models_to_test = {}
if args.model in ['LR', 'ALL']:
    models_to_test['Logistic Regression'] = LogisticRegression(max_iter=2000, random_state=42, C=args.lr_c)
if args.model in ['RF', 'ALL']:
    models_to_test['Random Forest'] = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
if args.model in ['MLP', 'ALL']:
    models_to_test['Multi-Layer Perceptron'] = MLPClassifier(hidden_layer_sizes=(100,), max_iter=2000, random_state=42)
if args.model in ['SVM', 'ALL']:
    models_to_test['Support Vector Machine'] = LinearSVC(max_iter=2000, random_state=42)
if args.model in ['NB', 'ALL']:
    models_to_test['Naive Bayes'] = MultinomialNB(alpha=args.nb_alpha)

for model_name, model in models_to_test.items():
    print(f"\n--- Training {model_name} ---")
    if model_name == 'Logistic Regression':
        print(f"Logistic Regression setting: C={args.lr_c:g}")
    if model_name == 'Naive Bayes':
        print(f"Naive Bayes setting: alpha={args.nb_alpha:g}")
    pipeline = make_pipeline(vectorizer, model)
    pipeline.fit(X_train, y_train)
    y_predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_predictions)
    print(f"\n*** Final {model_name} Accuracy: {accuracy * 100:.2f}% ***\n")
    print(f"Detailed Classification Report: {model_name}")
    print(classification_report(y_test, y_predictions, zero_division=0))

    # Append the results to the log file EXPERIMENTS.md
    with open("EXPERIMENTS.md", "a") as f:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        inputs_used = (
            f"Title + Description (TF-IDF analyzer {args.analyzer}; max {args.features}; "
            f"n-grams {args.ngram_min}-{args.ngram_max}; "
            "stratified 80/20 holdout, seed 42"
        )
        if model_name == 'Logistic Regression':
            inputs_used += f"; LR C={args.lr_c:g}"
        if model_name == 'Naive Bayes':
            inputs_used += f"; NB alpha={args.nb_alpha:g}"
        f.write(f"| {date_str} | {inputs_used}) | {model_name} | {accuracy * 100:.2f}% |\n")
    print(f"Results logged to EXPERIMENTS.md!")
