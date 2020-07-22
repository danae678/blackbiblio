import os
import random
from author_list import myList
from googleapiclient import discovery


class RecommendBook:
    def __init__(self):
        pass

    def get_book_payload(self):
        books_service = discovery.build(
            "books",
            "v1",
            # discoveryServiceUrl="https://www.googleapis.com/books/v1/volumes?q=",
            developerKey=os.environ["BOOKS_API_KEY"],
            cache_discovery=False,
        )
        author_search = random.choice(myList)
        i = random.randint(1, 4)  # gets random int for startindex
        volumes = books_service.volumes()
        return volumes.list(q=author_search, maxResults=1, startIndex=i).execute()
