import requests
from bs4 import BeautifulSoup
import difflib
import os

URL = "https://www.gsi.go.jp/BOUSAI/20240101_noto_earthquake.html"
PAGE_FILE = "latest_page.html"
PREVIOUS_PAGE_FILE = "previous_page.html"

def download_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def save_page(content, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def load_page(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    return None

def compare_pages(new_content, old_content):
    if old_content is None:
        print("No previous version to compare.")
        return False
    diff = difflib.unified_diff(
        old_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile="previous",
        tofile="current"
    )
    differences = list(diff)
    return differences

def main():
    new_page = download_page(URL)
    old_page = load_page(PREVIOUS_PAGE_FILE)
    differences = compare_pages(new_page, old_page)

    if differences:
        print("Changes detected:")
        for line in differences:
            print(line)
        save_page(new_page, PREVIOUS_PAGE_FILE)
    else:
        print("No changes detected.")

    save_page(new_page, PAGE_FILE)

if __name__ == "__main__":
    main()
