import requests
from bs4 import BeautifulSoup
import webbrowser
import streamlit as st

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
            st.error(f"Error: {e}")

        return urls

    def open_results(self, urls):
        for url in urls:
            webbrowser.open_new_tab(url)


def main():
    st.set_page_config(
        page_title="Search Result Opener",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Automated Search Result Opening System")

    st.markdown(
        """
        Enter a search query and choose how many search results you want to open automatically.
        """
    )

    query = st.text_input(
        "Enter Search Topic",
        placeholder="Machine Learning"
    )

    num_results = st.slider(
        "Number of Results",
        min_value=1,
        max_value=10,
        value=5
    )

    if st.button("Search and Open"):
        if query.strip() == "":
            st.warning("Please enter a search topic.")
            return

        opener = SearchResultOpener(query, num_results)
        urls = opener.get_results()

        if urls:
            st.success(f"{len(urls)} results found!")
            st.subheader("Search Results")

            for i, url in enumerate(urls, start=1):
                st.write(f"{i}. {url}")

            opener.open_results(urls)
            st.success("All search results opened successfully!")
        else:
            st.info("No search results were found. Try another query.")


if __name__ == "__main__":
    main()
