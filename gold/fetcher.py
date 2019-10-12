from abc import ABC, abstractmethod
from typing import List

from gold import Payment


class Fetcher(ABC):
    """
    Fetches payments from a source.
    """

    @abstractmethod
    def fetch(self) -> List[Payment]:
        """
        Get all payments from the source.
        """
        pass
