
import requests
from dotenv import load_dotenv
from app.classes.transactions import Transactions
from app.core.db import DbConnection
from bs4 import BeautifulSoup

load_dotenv()

BASE_HREF = 'https://quotes.toscrape.com/'

urls = []

def main():
    # make connect to db
    client = DbConnection().client
    db = client.book

    # truncate collections
    Transactions(db.quotes).deleteAll()
    Transactions(db.authors).deleteAll()

    # init first pagepoetry self add poetry-plugin-dotenv
    page = 1

    # parse pages
    while True:
        url = BASE_HREF + f"page/{page}"
        list_quotes = get_quotes(url, db)
        count_quotes = len(list_quotes)

        if count_quotes:
            db.quotes.insert_many(list_quotes)

        if(count_quotes <= 0):
            break

        # increment page (next page)
        page += 1

    print("\nScrapping - Done!")
        
def get_quotes(url, db):

    # pass global urls to author
    global urls

    print(f"scrap -> href: {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    list_quotes, list_authors = [], []
    for i in range(0, len(quotes)):

        list_quotes.append({
            "quote": quotes[i].text,
            "author": authors[i].text,
            "tags": [tag.text for tag in tags[i].find_all('a', class_='tag')]
        })

        url = authors[i].find_next_siblings()[0].get('href').lstrip('/')

        # check if we have current url to author
        if not url in urls:
            urls.append(url)
            list_authors.append(get_author(BASE_HREF + url))
            print(f"scrap -> href: {BASE_HREF + url}")

    if len(list_authors):
        db.authors.insert_many(list_authors)

    return list_quotes


def get_author(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    h3 = soup.find('h3')
    born_date = soup.find('span', class_='author-born-date')
    born_location = soup.find('span', class_='author-born-location')
    description = soup.find('div', class_='author-description')

    return {
        "fullname": h3.text,
        "born_date": born_date.text,
        "born_location": born_location.text,
        "description": description.text.strip()
    }

if __name__ == '__main__':
    main()