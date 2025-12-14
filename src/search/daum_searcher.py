import requests

from .base_searcher import BaseImageSearcher


class DaumImageSearcher(BaseImageSearcher):

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://dapi.kakao.com/v2/search/image"

    def search(self, query, num_results=5):
        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        params = {"query": query, "size": num_results}

        try:
            response = requests.get(self.base_url, params, headers=headers)
            response.raise_for_status()

            data = response.json()

            return [item["image_url"] for item in data.get("documents", [])]
        except Exception as e:
            print(f"Error during Daum image search: {e}")
            return []


if __name__ == "__main__":
    api_key = "YOUR_KAKAO_API_KEY"
    searcher = DaumImageSearcher(api_key)
    results = searcher.search("김병주 국회의원", num_results=3)
    for url in results:
        print(url)
