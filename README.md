
# Books Scraper

A Python web scraper that collects book titles and prices from
[Books to Scrape](https://books.toscrape.com/).

## Features

- Automatic pagination
- HTTP error handling and retry attempts
- HTML parsing with BeautifulSoup
- Missing-data validation
- Price conversion to numeric values
- CSV export with pandas
- Reusable functions and configurable settings

## Requirements

- Python 3.10 or newer
- Dependencies listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone https://github.com/luksssll/scraper.git
cd scraper
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

Run the scraper:

```bash
python main.py
```

The default configuration collects up to 10 pages and saves
the results to `books.csv`.

Change `MAX_PAGES` in `main.py` to adjust the limit.
Set `max_pages=None` in the `main()` call to scrape all
available pages.

## Output

The generated CSV contains:

- `title`: Book title
- `price`: Book price as a numeric value

## Disclaimer

This project is intended for educational purposes.
Always respect a website's terms of use and scraping policies.
