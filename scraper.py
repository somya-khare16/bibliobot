import re
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

from storage import save_to_csv, save_to_json

BASE_URL = "https://books.toscrape.com/"
WANTED_CATEGORIES = ["Philosophy","Psychology","Self Help","Art"]
RATINGS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

def scrape_category(page, name, url):
    books = []
    page.goto(url)

    while True:
        for card in page.locator("article.product_pod").all():
            title = card.locator("h3 a").get_attribute("title")

            price_text = card.locator(".price_color").inner_text()
            price = float(re.sub(r"[^\d.]", "", price_text))
            # means "replace everything that is not a digit or a dot with nothing". ^ inside the brackets means "not", and \d means "digit".

            rating_class = card.locator("p.star-rating").get_attribute("class")
            rating = RATINGS[rating_class.split()[-1]]

            books.append(
                {"title": title, "category": name, "price": price, "rating": rating}
            )

        if page.locator("li.next a").count() == 0:
            break
        page.locator("li.next a").click()
        page.wait_for_load_state()
        # wait_for_load_state() pauses until the new page is loaded. Without that pause, the loop could read the old page again.

    return books

def main():
    all_books = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(BASE_URL)

        category_links = {}
        for link in page.locator("div.side_categories ul ul a").all():
            name = link.inner_text().strip()
            # strip() is there so the name matches your wanted list, it removes the extra spaces
            if name in WANTED_CATEGORIES:
                category_links[name] = urljoin(page.url, link.get_attribute("href"))

        missing = set(WANTED_CATEGORIES) - set(category_links)
        if missing:
            print(f"Warning: categories not found on the site: {missing}")

        for name, url in category_links.items():
            books = scrape_category(page, name, url)
            all_books.extend(books)
            print(f"Scraped {len(books)} books from {name}")

        browser.close()


    save_to_csv(all_books)
    save_to_json(all_books)
    print(f"Done! {len(all_books)} books saved to books.csv and books.json")

if __name__ == "__main__":
    main()