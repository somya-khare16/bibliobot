# 📚 Bibliobot

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Playwright](https://img.shields.io/badge/Playwright-automation-green)

A Python + Playwright bot that scrapes books by category from an online bookstore, cleans the data, exports it to CSV and JSON, and analyzes the data.

## What it does

1. **Scrapes** books from [books.toscrape.com](https://books.toscrape.com) (a practice site built for scraping), across multiple pages per category
2. **Cleans** the data: prices become numbers, star ratings become 1 to 5
3. **Saves** the results to `books.csv` and `books.json`
4. **Analyzes** the data with plain Python: best-value books, a summary per category, and the cheapest 5-star books

Categories scraped: Self Help, Art, Psychology, Philosophy (editable in `scraper.py`).

## Project structure

```
bibliobot/
├── scraper.py        # Playwright bot: collects books
├── storage.py        # Saves books to CSV and JSON
├── analysis.py       # Loads the CSV and answers questions
├── books.csv         # Sample output
├── books.json        # Sample output
└── requirements.txt
```

## How to run

```powershell
git clone https://github.com/somya-khare16/bibliobot.git
cd bibliobot
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium

python scraper.py     # collect the data
python analysis.py    # analyze it
```

Categories are set in `WANTED_CATEGORIES` in `scraper.py`.

## Sample output

```
Scraped 11 books from Philosophy
Scraped 8 books from Art
Scraped 7 books from Psychology
Scraped 5 books from Self Help
Done! 31 books saved to books.csv and books.json
```

```
Summary per category:
Philosophy: 11 books | avg price £33.56 | avg rating 2.4
Art: 8 books | avg price £38.52 | avg rating 3.6
```

## Design notes

- **Pagination:** the scraper keeps clicking "next" until the button disappears, so categories of any size work.
- **No duplicates:** each run overwrites the output files, so re-running gives identical results.
- **Missing categories:** if a name in `WANTED_CATEGORIES` isn't found on the site, the bot prints a warning instead of silently skipping it.
- **Verified output:** book counts per category were checked against the website.

## Note

Data comes from [books.toscrape.com](https://books.toscrape.com), a demo site built for scraping practice. Its prices and ratings are randomly generated, so the analysis demonstrates the pipeline rather than real book quality.