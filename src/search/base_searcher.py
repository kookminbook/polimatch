from abc import ABC, abstractmethod


class BaseImageSearcher(ABC):

    @abstractmethod
    def search(self, query, num_results=5):
        """Search for images based on the query.

        Args:
            query (str): The search query.
            num_results (int): The number of results to return.

        Returns:
            list: A list of image URLs.
        """
        pass
