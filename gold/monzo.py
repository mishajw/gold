from typing import List

from gold import Fetcher, Payment


class MonzoFetcher(Fetcher):
    def fetch(self) -> List[Payment]:
        raise NotImplementedError()
