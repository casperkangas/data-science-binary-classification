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
    # Helper mapping for star ratings for later conversion to integer
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
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
        
        # Extract Price (raw text, will be cleaned later)
        price = article.find('p', class_='price_color').text.strip()
        
        # Extract Star Rating (converted to integer)
        rating_class = article.find('p', class_='star-rating')['class'][1]
        star_rating = rating_map.get(rating_class, 0)
        
        # Extract In-Stock Availability
        availability = article.find('p', class_='instock').text.strip()
        
        books_data.append({
            'title': title,
            'category': category,
            'image_url': img_url,
            'price': price,
            'star_rating': star_rating,
            'availability': availability
        })
        
    return books_data

if __name__ == "__main__":
    print("Fetching Fiction category...")
    soup = get_soup(FICTION_URL)
    books = extract_books_from_page(soup, "Fiction")
    print(f"Successfully extracted {len(books)} books!")
    print("First book sample:", books[0])
