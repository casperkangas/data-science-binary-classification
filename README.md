# Data Science Project: Binary Classification

This project is a binary classification task to predict whether a book is "Fiction" or "Nonfiction" using data scraped from [Books to Scrape](http://books.toscrape.com/).

## Setup Instructions

To ensure reproducibility and avoid conflicts with system-wide packages, this project uses a Python virtual environment. Packages are kept up-to-date by `dependabot`.

1. **Create and activate the virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Running the Pipeline

### 1. Web Scraping

To scrape book titles, descriptions, categories, and cover images from Books to Scrape:

```bash
python scraper.py
```

This extracts data for fiction and nonfiction categories and saves raw results to `books_data_full.csv` while archiving cover images to `data/images/`.

### 2. Data Cleaning

To repair encoding artifacts (UTF-8 mojibake), normalize text, strip irregular whitespace, and prune empty rows:

```bash
python clean_data.py
```

This produces `books_data_clean.csv`, which is used for model training and evaluation.

### 3. Model Training & Evaluation

To run the training script with default baseline settings (Logistic Regression, 100 word features):

```bash
python model_training.py
```

### Replicating the Best Result (80% Accuracy)

To reproduce the peak-performing model from the report (Random Forest utilizing character n-grams with word boundaries and 1 000 features):

```bash
python model_training.py --model RF --analyzer char_wb --features 1000
```

### Advanced Usage & Available Flags

You can customize the model and feature engineering pipeline on the fly using command-line arguments:

```bash
# Evaluate all models with character n-grams
python model_training.py --model ALL --analyzer char_wb --features 1000

# Run Naive Bayes with custom smoothing
python model_training.py --model NB --nb-alpha 0.5

# Run Logistic Regression with tuned regularization
python model_training.py --model LR --lr-c 10.0
```

#### Command-Line Options

- `--model`: Algorithm selection.
  - Choices: `LR` (Logistic Regression), `RF` (Random Forest), `MLP` (Multi-Layer Perceptron), `SVM` (Support Vector Machine), `NB` (Naive Bayes), or `ALL` (runs all models sequentially).
- `--analyzer`: Feature extraction mode.
  - Choices: `word` (word-level tokens, default) or `char_wb` (character n-grams within word boundaries).
- `--features`: Maximum number of TF-IDF terms to track (e.g. `100`, `500`, `1000`).
- `--ngram-min` / `--ngram-max`: N-gram size boundaries (defaults to 1-1 for words, 3-5 for characters).
- `--lr-c`: Regularization strength for Logistic Regression (default: `1.0`).
- `--nb-alpha`: Additive Laplace smoothing parameter for Naive Bayes (default: `1.0`).

All experimental runs and results are automatically logged to `EXPERIMENTS.md`.
