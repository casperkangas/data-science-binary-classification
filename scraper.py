import requests
from bs4 import BeautifulSoup

# Category URLs
FICTION_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
NONFICTION_URL = "http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"

def get_soup(url):
    """
    Fetches the HTML content from the given URL and parses it using BeautifulSoup.
    """
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

if __name__ == "__main__":
    # DEBUG: Test the function with the Fiction category
    print("Fetching Fiction category...")
    soup = get_soup(FICTION_URL)
    
    # DEBUG: Print the page title to verify it worked
    print(f"Success! Page Title: {soup.title.text.strip()}")
