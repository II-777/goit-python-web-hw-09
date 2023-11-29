from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import aiohttp
import json
from load_data import LoadData


async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()


def scrape_quotes_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all('div', class_="quote")
    quotes_data = []

    for card in cards:
        text = card.find('span', class_="text").get_text(strip=True)
        author = card.find('small', class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True)
                for tag in card.find_all('a', class_="tag")]

        quote_info = {
            "tags": tags,
            "author": author,
            "quote": text
        }

        quotes_data.append(quote_info)

    return quotes_data


async def scrape_quotes_multi_page(target_url):
    async with aiohttp.ClientSession() as session:
        url = target_url
        quotes = []

        print("SCRAPING QUOTES:")
        print("#" + '-' * 24)
        while True:
            html = await fetch_page(session, url)
            current_quotes = scrape_quotes_one_page(html)
            quotes += current_quotes
            print(f"[+] Scraped quotes from: {url}")

            soup = BeautifulSoup(html, "html.parser")
            next_link = soup.find('li', class_="next")
            if next_link:
                url = urljoin(target_url, next_link.find('a')['href'])
            else:
                break

        return quotes


async def scrape_authors_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    author_details = soup.find('div', class_="author-details")

    fullname = author_details.find(
        'h3', class_="author-title").get_text(strip=True)
    born_date = author_details.find(
        'span', class_="author-born-date").get_text(strip=True)
    born_location = author_details.find(
        'span', class_="author-born-location").get_text(strip=True)
    description = author_details.find(
        'div', class_="author-description").get_text(strip=True)

    author_data = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

    return author_data


async def scrape_authors_multi_page(target_url):
    async with aiohttp.ClientSession() as session:
        url = target_url
        authors = set()

        print("\nSCRAPING AUTHORS:")
        print("#" + '-' * 24)
        while True:
            html = await fetch_page(session, url)
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.find_all('div', class_="quote")

            for card in cards:
                author_link = card.find('a')['href']
                target_url = urljoin(target_url, author_link)
                authors.add(target_url)

            next_link = soup.find('li', class_="next")
            if next_link:
                url = urljoin(target_url, next_link.find('a')['href'])
            else:
                break

        authors_data = []
        for target_url in authors:
            html = await fetch_page(session, target_url)
            author_info = await scrape_authors_one_page(html)
            print(f"[+] Scraped authors from: {target_url}")
            authors_data.append(author_info)

        return authors_data

if __name__ == "__main__":
    base_url = 'http://quotes.toscrape.com'

    loop = asyncio.get_event_loop()
    result_quotes = loop.run_until_complete(scrape_quotes_multi_page(base_url))
    result_authors = loop.run_until_complete(
        scrape_authors_multi_page(base_url))

    print("#" + '-' * 24)
    print(f"[!] Total of {len(result_quotes)} quotes written to 'quotes.json'")
    with open('quotes.json', 'w', encoding='utf-8') as json_file:
        json.dump(result_quotes, json_file, ensure_ascii=False, indent=2)

    print(
        f"[!] Total of {len(result_authors)} authors written to 'authors.json'")
    with open('authors.json', 'w', encoding='utf-8') as json_file:
        json.dump(result_authors, json_file, ensure_ascii=False, indent=2)
    
    LoadData()
