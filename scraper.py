import requests
from bs4 import BeautifulSoup

# Category URLs
BASE_URL = "http://books.toscrape.com/"
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

def extract_books_from_page(soup, category):
    """
    Extracts book data from the parsed HTML page and returns a list of dictionaries containing the extracted data.
    """
    books_data = []
    # Find all the article tags that wrap each book
    articles = soup.find_all('article', class_='product_pod')
    
    for article in articles:
        # Extract Title
        title = article.find('h3').find('a')['title']
        
        # Extract Image URL and make it absolute
        img_src = article.find('img', class_='thumbnail')['src']
        # Replace relative path parts to build full URL
        img_url = BASE_URL + img_src.replace('../', '')
        
        books_data.append({
            'title': title,
            'category': category,
            'image_url': img_url
        })
        
    return books_data

if __name__ == "__main__":
    print("Fetching Fiction category...")
    soup = get_soup(FICTION_URL)
    books = extract_books_from_page(soup, "Fiction")
    print(f"Successfully extracted {len(books)} books!")
    print("First book sample:", books[0])
