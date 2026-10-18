
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx
import pandas as pd
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
MAX_PAGES = 10
MAX_ATTEMPTS = 3
TIMEOUT = 10

OUTPUT_FILE = Path("books.csv")


def fetch_page(client, url):
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.get(url)
            response.raise_for_status()

            return response.text

        except httpx.HTTPError as error:
            print(
                f"Request failed "
                f"({attempt}/{MAX_ATTEMPTS}): {error}"
            )

            if attempt < MAX_ATTEMPTS:
                time.sleep(attempt)

    print(f"Giving up on: {url}")
    return None


def extract_books(html):
    """Extract book titles and prices from HTML."""

    soup = BeautifulSoup(html, "lxml")
    book_elements = soup.select("article.product_pod")

    books = []

    for book in book_elements:
        title_element = book.select_one("h3 a")
        price_element = book.select_one(".price_color")

        if title_element is None or price_element is None:
            print("Skipping a book with missing information.")
            continue

        title = (
            title_element.get("title")
            or title_element.get_text(strip=True)
        )

        price_text = price_element.get_text(strip=True)
        price_text = price_text.replace("£", "").strip()

        try:
            price = float(price_text)
        except ValueError:
            print(f"Invalid price for book: {title}")
            continue

        books.append({
            "title": title,
            "price": price,
        })

    return books


def get_next_page(html, current_url):

    soup = BeautifulSoup(html, "lxml")
    next_link = soup.select_one("li.next a")

    if next_link is None:
        return None

    next_href = next_link.get("href")

    if not next_href:
        return None

    return urljoin(current_url, next_href)


def scrape_books(max_pages=None):

    all_books = []
    current_url = BASE_URL
    pages_scraped = 0

    with httpx.Client(timeout=TIMEOUT) as client:
        while current_url:
            if max_pages is not None and pages_scraped >= max_pages:
                break

            print(f"Fetching: {current_url}")

            html = fetch_page(client, current_url)

            if html is None:
                break

            page_books = extract_books(html)
            all_books.extend(page_books)

            pages_scraped += 1
            print(
                f"Page {pages_scraped}: "
                f"{len(page_books)} books extracted."
            )

            current_url = get_next_page(html, current_url)

    print(f"Pages scraped: {pages_scraped}")
    print(f"Total books collected: {len(all_books)}")

    return all_books


def save_to_csv(books, output_file):

    columns = ["title", "price"]
    df = pd.DataFrame(books, columns=columns)

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"CSV saved to: {output_file.resolve()}")
    print(f"File size: {output_file.stat().st_size} bytes")

    return df


def main():
    books = scrape_books(max_pages=MAX_PAGES)
    df = save_to_csv(books, OUTPUT_FILE)

    print("\nFirst five books:")
    print(df.head())

    print(f"\nDataset shape: {df.shape}")


if __name__ == "__main__":
    main()
