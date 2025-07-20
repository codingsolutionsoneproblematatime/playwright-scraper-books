# Playwright Book Scraper

This project is a fully automated web scraper built with **Python** and **Playwright**. It extracts book data from all 50 pages of [Books to Scrape](https://books.toscrape.com), converts prices from GBP to USD using live rates from ExchangeRate API, and exports the results to Excel.

---

## Features

- Automates browser scraping using Playwright (headless Chromium)
- Scrapes all 50 pages from the site
- Extracts title, price (GBP & USD), availability, and star rating
- Converts prices using live GBP --> USD exchange rate via ExchangeRate API
- Adds a unique `BookID` (GUID) for each record
- Tracks script execution time
- Saves results to Excel using `pandas` and `openpyxl`
- Uses `.env` file for secure API key management

---

## Tech Stack

- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- `pandas`, `requests`, `openpyxl`
- `python-dotenv` + `.env` file
- ExchangeRate API (free tier)
- Git + GitHub for version control

---

## How to Run

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/playwright-scraper-books.git
cd playwright-scraper-books
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m playwright install
```

If you don’t have a requirements.txt, install manually:

```bash
pip install playwright pandas requests python-dotenv openpyxl
```

### 3. Set Up Your .env

Create a file named .env in the project folder and add:

```ini
EXCHANGE_RATE_API_KEY=your_api_key_here
```

Get your free API key from https://www.exchangerate-api.com.

### 4. Run the Script

```bash
python bookscan_scraper.py
```

You’ll see browser activity, price conversion, and a book_data.xlsx file created when complete.

