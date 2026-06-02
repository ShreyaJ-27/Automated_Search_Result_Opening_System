import requests
from bs4 import BeautifulSoup
import webbrowser

class SearchResultOpener:

    def __init__(self, query, num_results):
        self.query = query
        self.num_results = num_results

    def get_results(self):
        urls = []

        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.post(
                "https://html.duckduckgo.com/html",
                data={"q": self.query},
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.select("a.result__a"):
                href = link.get("href")
                if href and href.startswith("http") and "duckduckgo.com" not in href:
                    urls.append(href)
                    if len(urls) >= self.num_results:
                        break

        except Exception as e:
            print(f"Error: {e}")

        return urls

    def open_results(self, urls):
        for url in urls:
            webbrowser.open_new_tab(url)


def main():
    print("=" * 50)
    print("🔍 Automated Search Result Opening System")
    print("=" * 50)
    print()

    query = input("Enter Search Topic: ").strip()

    if query == "":
        print("Please enter a search topic.")
        return

    while True:
        try:
            num_results = int(input("Number of Results (1-10): "))
            if 1 <= num_results <= 10:
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    print("\nSearching...")
    opener = SearchResultOpener(query, num_results)
    urls = opener.get_results()

    if urls:
        print(f"\n✓ {len(urls)} results found!")
        print("\nSearch Results:")
        print("-" * 50)

        for i, url in enumerate(urls, start=1):
            print(f"{i}. {url}")

        print("-" * 50)
        open_choice = input("\nOpen these results in browser? (yes/no): ").strip().lower()
        if open_choice in ['yes', 'y']:
            opener.open_results(urls)
            print("✓ All search results opened successfully!")
        else:
            print("Results not opened.")
    else:
        print("\n✗ No search results were found. Try another query.")


if __name__ == "__main__":
    main()
