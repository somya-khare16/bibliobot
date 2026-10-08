import csv

def load_books(filename="books.csv"):
    with open(filename, newline="", encoding="utf-8") as f:
        books = list(csv.DictReader(f))

    for book in books:
        book["price"] = float(book["price"])
        book["rating"] = int(book["rating"])

    return books

def best_value_books(books, max_price=30, min_rating=4):
    good = [
        book for book in books
        if book["price"] < max_price and book["rating"] >= min_rating
    ]
    return sorted(good, key=lambda book: (-book["rating"], book["price"]))
# lambda book: ... is a tiny function written on one line. It means "for each book, use this value for sorting". It has no name because we only need it here.


def category_summary(books):
    groups = {}
    for book in books:
        category = book["category"]
        if category not in groups:
            groups[category] = []
        groups[category].append(book)

    summary = []
    for category, items in groups.items():
        summary.append({
            "category": category,
            "count": len(items),
            "avg_price": sum(b["price"] for b in items) / len(items),
            "avg_rating": sum(b["rating"] for b in items) / len(items),
        })
    return summary
# It's indented at the function level, outside the loop, so it runs once, after every category is done.

def cheapest_five_star(books, limit=5):
    five_star = [book for book in books if book["rating"]==5]
    # make a list of every book in books, if its rating equals 5.
    return sorted(five_star, key=lambda book: book["price"])[:limit]


if __name__ == "__main__":
    books = load_books()
    print("Top-rated books under £30:")
    for book in best_value_books(books):
        print(f"{book['rating']} stars | £{book['price']:.2f} | {book['title']} ({book['category']})")
        # :.2f means "show exactly 2 digits after the decimal point"
    print("\nSummary per category:")
    for row in category_summary(books):
        print(f"{row['category']}: {row['count']} books | avg price £{row['avg_price']:.2f} | avg rating {row['avg_rating']:.1f}")
    print("\nCheapest 5-star books:")
    for book in cheapest_five_star(books):
        print(f"£{book['price']:.2f} | {book['title']} ({book['category']})")