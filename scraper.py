import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Category URLs
BASE_URL = "http://books.toscrape.com/"
FICTION_URL = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
NONFICTION_URL = "http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def download_image(img_url, filename, output_dir="data/images"):
    os.makedirs(output_dir, exist_ok=True)
    local_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(local_path):
        try:
            response = requests.get(img_url, stream=True)
            response.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
            return None
    return local_path

def scrape_book_details(book_url, category_name, book_id):
    """
    Visits an individual book's page to extract full details, including the description and image.
    """
    soup = get_soup(book_url)
    
    # Title
    title = soup.find('div', class_='col-sm-6 product_main').find('h1').text.strip()
    
    # Description
    desc_tag = soup.find('div', id='product_description')
    description = desc_tag.find_next_sibling('p').text.strip() if desc_tag else ""
    
    # Image URL
    img_src = soup.find('div', class_='item active').find('img')['src']
    img_url = urljoin(book_url, img_src)
    
    # Download the Image
    image_filename = f"book_{book_id:04d}.jpg"
    local_image_path = download_image(img_url, image_filename)
    
    return {
        'title': title,
        'category': category_name,
        'description': description,
        'image_url': img_url,
        'local_image_path': local_image_path
    }

def scrape_category(start_url, category_name, start_id=0):
    all_books = []
    current_url = start_url
    current_id = start_id
    
    while current_url:
        print(f"Scraping category page: {current_url}")
        soup = get_soup(current_url)
        
        # Get all book links on this category page
        articles = soup.find_all('article', class_='product_pod')
        for article in articles:
            book_href = article.find('h3').find('a')['href']
            book_url = urljoin(current_url, book_href)
            
            print(f"  -> Scraping details for book {current_id}...")
            book_data = scrape_book_details(book_url, category_name, current_id)
            all_books.append(book_data)
            current_id += 1
            
        # Check for the next page
        next_btn = soup.find('li', class_='next')
        if next_btn:
            next_href = next_btn.find('a')['href']
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None
            
    return all_books, current_id

if __name__ == "__main__":
    print("Starting data scraping...")
    
    fiction_books, next_id = scrape_category(FICTION_URL, "Fiction", start_id=0)
    print(f"Successfully extracted {len(fiction_books)} Fiction books!")
    
    nonfiction_books, final_id = scrape_category(NONFICTION_URL, "Nonfiction", start_id=next_id)
    print(f"Successfully extracted {len(nonfiction_books)} Nonfiction books!")
    
    # Combine data
    all_books_data = fiction_books + nonfiction_books
    
    # Save to CSV
    df = pd.DataFrame(all_books_data)
    csv_filename = "books_data_full.csv"
    df.to_csv(csv_filename, index=False)
    print(f"\nSaved {len(all_books_data)} total books to {csv_filename}!")