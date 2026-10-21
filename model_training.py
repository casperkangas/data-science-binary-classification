import pandas as pd
import datetime
import argparse
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Command-line argument parsing, which allows the user to run: python model_training.py --model RF --features 150
parser = argparse.ArgumentParser(description="Train a book classification model.")
parser.add_argument('--model', type=str, choices=['LR', 'RF', 'MLP', 'SVM', 'NB', 'ALL'], default='LR', help="Choose LR (Logistic Regression), RF (Random Forest), MLP (Multi-Layer Perceptron), SVM (Support Vector Machine), NB (Naive Bayes), or ALL")
parser.add_argument('--features', type=int, default=100, help="Max number of words for TF-IDF to track")
parser.add_argument('--lr-c', type=float, default=1.0, help="Regularization strength for Logistic Regression (smaller values mean stronger regularization)")
parser.add_argument('--ngram-min', type=int, default=1, help="Minimum word n-gram size for TF-IDF")
parser.add_argument('--ngram-max', type=int, default=1, help="Maximum word n-gram size for TF-IDF")
parser.add_argument('--cv-folds', type=int, default=5, help="Number of stratified cross-validation folds")
parser.add_argument('--cv-repeats', type=int, default=5, help="Number of times to repeat stratified cross-validation")
args = parser.parse_args()

if args.features < 1:
    parser.error("--features must be at least 1")
if args.lr_c <= 0:
    parser.error("--lr-c must be greater than 0")
if args.ngram_min < 1 or args.ngram_max < 1:
    parser.error("--ngram-min and --ngram-max must be at least 1")
if args.ngram_min > args.ngram_max:
    parser.error("--ngram-min cannot be greater than --ngram-max")
if args.cv_folds < 2:
    parser.error("--cv-folds must be at least 2")
if args.cv_repeats < 1:
    parser.error("--cv-repeats must be at least 1")

# Load the cleaned dataset
print("Loading cleaned dataset...")
df = pd.read_csv("books_data_clean.csv")

# Combine 'title' and 'description' for maximum text context, with fillna("") to handle any missing values
df['combined_text'] = df['title'].fillna("") + " " + df['description'].fillna("")

# Predict the 'category' based on the combined text
X_text = df['combined_text']  # Input feature
y_target = df['category']   # Target label (the category)

print("Converting text into mathematical features (TF-IDF)...")

# Initialize the vectorizer, which will be fitted separately inside each training fold
# max_features limits the vocabulary to the most frequent terms, while ngram_range adds adjacent word combinations when --ngram-max is greater than 1
vectorizer = TfidfVectorizer(
    max_features=args.features,
    stop_words='english',
    ngram_range=(args.ngram_min, args.ngram_max),
)
cv = RepeatedStratifiedKFold(
    n_splits=args.cv_folds,
    n_repeats=args.cv_repeats,
    random_state=42,
)
scoring = {
    'accuracy': 'accuracy',
    'balanced_accuracy': 'balanced_accuracy',
    'macro_f1': 'f1_macro',
}

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
    models_to_test['Naive Bayes'] = MultinomialNB()

for model_name, model in models_to_test.items():
    print(f"\n--- Training {model_name} ---")
    pipeline = make_pipeline(vectorizer, model)
    scores = cross_validate(
        pipeline,
        X_text,
        y_target,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
    )

    print(f"Results over {args.cv_folds} folds x {args.cv_repeats} repeats:")
    for metric_name, label in (
        ('accuracy', 'Accuracy'),
        ('balanced_accuracy', 'Balanced accuracy'),
        ('macro_f1', 'Macro F1'),
    ):
        fold_scores = scores[f'test_{metric_name}']
        print(f"{label}: {fold_scores.mean() * 100:.2f}% +/- {fold_scores.std() * 100:.2f}%")

    # Append the results to the log file EXPERIMENTS.md
    with open("EXPERIMENTS.md", "a") as f:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        inputs_used = (
            f"Title + Description (TF-IDF max {args.features}; "
            f"word n-grams {args.ngram_min}-{args.ngram_max}; "
            f"{args.cv_folds}-fold x {args.cv_repeats} repeated stratified CV"
        )
        if model_name == 'Logistic Regression':
            inputs_used += f"; LR C={args.lr_c:g}"
        accuracy_scores = scores['test_accuracy']
        accuracy_summary = f"{accuracy_scores.mean() * 100:.2f}% +/- {accuracy_scores.std() * 100:.2f}%"
        f.write(f"| {date_str} | {inputs_used}) | {model_name} | {accuracy_summary} |\n")
    print(f"Results logged to EXPERIMENTS.md!")
