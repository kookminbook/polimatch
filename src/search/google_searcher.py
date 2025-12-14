import requests

from .base_searcher import BaseImageSearcher


class GoogleImageSearcher(BaseImageSearcher):

    def __init__(self, api_key, prog_search_engine_id):
        self.api_key = api_key
        self.prog_search_engine_id = prog_search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search(self, query, num_results=5):
        params = {
            "q": query,
            "key": self.api_key,
            "cx": self.prog_search_engine_id,
            "searchType": "image",
            "num": num_results,
        }

        try:
            response = requests.get(self.base_url, params)
            response.raise_for_status()

            data = response.json()

            return [item["link"] for item in data.get("items", [])]
        except Exception as e:
            print(f"Error during Google image search: {e}")
            return []


if __name__ == "__main__":
    api_key = "YOUR_GOOGLE_API_KEY"
    prog_search_engine_id = "YOUR_GOOGLE_PROGRAMMABLE_SEARCH_ENGINE_ID"
    searcher = GoogleImageSearcher(api_key, prog_search_engine_id)
    results = searcher.search("김병주 국회의원", num_results=3)
    for url in results:
        print(url)
