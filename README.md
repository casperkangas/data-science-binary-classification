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

# Execute the scraper
python scraper.py
```
