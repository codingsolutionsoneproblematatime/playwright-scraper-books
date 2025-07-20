import os
import requests
import pandas as pd
import uuid
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# load .env file
load_dotenv()

# fetch current exchange rate from gbp to usd
def get_gbp_to_usd_rate():
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    fallback_rate = 1.30

    if not api_key:
        print(f"no api key found. will use fallback rate of {fallback_rate}.")
        return fallback_rate

    try:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/GBP"
        response = requests.get(url, timeout=10)
        data = response.json()
        rate = data["conversion_rates"]["USD"]
        print(f"live exchange rate loaded: 1 gbp = {rate} usd")
        return rate
    except Exception as e:
        print(f"failed to fetch exchange rate. using fallback rate {fallback_rate}. reason: {e}")
        return fallback_rate

# scrape all 50 pages of book data from books.toscrape.com
def scrape_all_books():
    conversion_rate = get_gbp_to_usd_rate()
    books_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        base_url = "https://books.toscrape.com/catalogue/page-{}.html"

        for page_num in range(1, 51):  # site has 50 pages
            url = base_url.format(page_num)
            page.goto(url)

            books = page.locator("article.product_pod")
            count = books.count()

            for i in range(count):
                title = books.nth(i).locator("h3 a").get_attribute("title")
                price_text = books.nth(i).locator(".price_color").inner_text()
                price_gbp = float(price_text.replace("£", ""))
                price_usd = round(price_gbp * conversion_rate, 2)
                availability = books.nth(i).locator(".availability").inner_text().strip()
                rating_class = books.nth(i).locator("p.star-rating").get_attribute("class")
                rating = rating_class.replace("star-rating", "").strip()

                books_data.append({
                    "BookID": str(uuid.uuid4()),  # generate unique id for each book
                    "Title": title,
                    "Price GBP": price_gbp,
                    "Price USD": price_usd,
                    "Availability": availability,
                    "Rating": rating
                })

            print(f"scraped page {page_num} with {count} books")

        browser.close()

    return books_data

# export book data to excel
def save_to_excel(books_data, filename="book_data.xlsx"):
    df = pd.DataFrame(books_data)
    df.to_excel(filename, index=False, engine="openpyxl")
    print(f"saved {len(df)} books to {filename}")

# run everything and track total runtime
if __name__ == "__main__":
    start_time = time.time()

    books = scrape_all_books()
    save_to_excel(books)

    end_time = time.time()
    duration = end_time - start_time
    print(f"script completed in {duration:.2f} seconds")
