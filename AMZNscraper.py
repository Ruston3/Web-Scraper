# Imports
import sys
from os import path
import csv
import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://www.amazon.co.uk/s?k=solar+panel"
PAGES_TO_SCRAPE = 1
HEADERS = {
    'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64)'
                    'AppleWebKit/537.36 (KHTML, like Gecko)'
                    'Chrome/44.0.2403.157 Safari/537.36'),
    'Accept-Language': 'en-US, en;q=0.5'
}

def parse(html):
# Returns a list of a dictionary of parsed products
    soup = BeautifulSoup(html, "html.parser")
    return [parse_product(article) for article in soup.find_all('div', class_= 'template=SEARCH_RESULTS')]


def parse_product(article):
# Returns a dictionary with product name, price, number of reviews and the average review score for the product
    name = article.find('span', class_= 'a-size-base-plus').string.strip()
    price = article.find('span', class_= 'a-offscreen').string.strip()
    return {'name': name, 'price': price}


def write_csv(search, products):
# writes info in lists to a CSV file
    with open(f'log/{search}.csv', 'w') as price_file:
        keys = products[0].keys()
        writer = csv.DictWriter(price_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)

def scrape_from_internet(search_term, start=1):
# Use requests to scrape HTML from a given page
    print(f"Scraping page {start}")
    response = requests.get(
        SEARCH_URL+f'{search_term}&page={start}',
        headers=HEADERS,
        )
    # Check the reponse history for re-direct
    if response.history:
        return None
    return response.text


def main():
    if len(sys.argv) > 1:
        search_term = sys.argv[1]
        products = []
        for page in range(PAGES_TO_SCRAPE):
            response = scrape_from_internet(search_term, page+1)
            if response:
                products += parse(response)
            else:
                print('no response')
                break

        print(len(products))
        write_csv(search_term, products)
        print(f"Wrote price results to log/{search_term}.csv")
    else:
        print('Usage: python solar_scraper.py SEARCH_TERM')
        sys.exit(0)


if __name__ == '__main__':
    main()
