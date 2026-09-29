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

## Running the Scraper

To run the web scraper and extract the book data:

```bash
# Make sure the virtual environment is active
source venv/bin/activate

# Run the scraper to get the initial CSV file
python scraper.py

# Download the physical image files
python download_images.py
```

## Training the Model

Once the data is scraped and cleaned, you can train the machine learning algorithms to classify books as Fiction or Nonfiction by running the `model_training.py` script.

### Basic Usage (Defaults)

To run the training script with the default settings, simply execute:

```bash
python model_training.py
```

**Default Settings:** If no arguments are provided, the script defaults to running a **Logistic Regression** model (`LR`) and limits the TF-IDF keyword extraction to a maximum of **100 features** (keywords).

### Advanced Usage (Command-Line Flags)

You can customize the script on the fly by passing flags directly in your terminal. This is highly recommended for experimenting with different model configurations.

```bash
# Run a Random Forest model with 200 TF-IDF features
python model_training.py --model RF --features 200

# Test both models with 50 TF-IDF features
python model_training.py --model ALL --features 50
```

#### Available Flags

- `--model`: Selects the machine learning algorithm
  - Options: `LR` (Logistic Regression), `RF` (Random Forest), or `ALL` (runs both models sequentially for direct comparison).
- `--features`: Defines the maximum number of words for the TF-IDF vectorizer to track.
  Accepts any integer (e.g., `50`, `100`, `500`). Lower numbers can help prevent overfitting on small datasets.
