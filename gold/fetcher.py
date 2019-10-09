from abc import ABC, abstractmethod
from typing import List

from gold import Payment


class Fetcher(ABC):
    @abstractmethod
    def fetch(self) -> List[Payment]:
        pass
