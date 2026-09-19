import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Category URLs
BASE_URL = "http://books.toscrape.com/"
FICTION_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
NONFICTION_URL = "http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"

def get_soup(url):
    # Fetches the HTML content from the given URL and parses it using BeautifulSoup.
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors
    
    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_books_from_page(soup, category):
    # Extracts book data from the parsed HTML page and returns a list of dictionaries containing the extracted data.
    
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

def scrape_category(start_url, category_name):
    # Scrapes all pages of a given category and returns a list of all book dictionaries.
    all_books = []
    current_url = start_url
    
    while current_url:
        print(f"Scraping {category_name}: {current_url}")
        soup = get_soup(current_url)
        books_on_page = extract_books_from_page(soup, category_name)
        all_books.extend(books_on_page)
        
        # Check for the next page
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_href = next_btn.find('a')['href']
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None  # Reached the last page
            
    return all_books

if __name__ == "__main__":
    print("Starting data scraping...")
    
    # Scrape Fiction
    fiction_books = scrape_category(FICTION_URL, "Fiction")
    print(f"Successfully extracted {len(fiction_books)} Fiction books!")
    
    # Scrape Nonfiction
    nonfiction_books = scrape_category(NONFICTION_URL, "Nonfiction")
    print(f"Successfully extracted {len(nonfiction_books)} Nonfiction books!")
    
    # Combine the scraped data
    all_books_data = fiction_books + nonfiction_books
    
    # Convert to Pandas DataFrame and save to CSV
    df = pd.DataFrame(all_books_data)
    csv_filename = "books_data.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nSaved {len(all_books_data)} total books to {csv_filename}!")
