import csv
import json

FIELDS = ["title","category","price","rating"]

def save_to_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(books)

def save_to_json(books, filename="books.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
        