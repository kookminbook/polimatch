import requests

from .base_searcher import BaseImageSearcher


class NaverImageSearcher(BaseImageSearcher):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://openapi.naver.com/v1/search/image"

    def search(self, query, num_results=5):
        headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }
        params = {"query": query, "display": num_results}

        try:
            response = requests.get(self.base_url, params, headers=headers)
            response.raise_for_status()

            data = response.json()

            return [item["link"] for item in data.get("items", [])]
        except Exception as e:
            print(f"Error during Naver image search: {e}")
            return []


if __name__ == "__main__":
    client_id = "YOUR_NAVER_CLIENT_ID"
    client_secret = "YOUR_NAVER_CLIENT_SECRET"
    searcher = NaverImageSearcher(client_id, client_secret)
    results = searcher.search("김병주 국회의원", num_results=3)
    for url in results:
        print(url)
