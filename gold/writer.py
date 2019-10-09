from abc import ABC, abstractmethod
from typing import List

from gold import Fetcher


class Writer(ABC):
    @abstractmethod
    def write(self, fetchers: List[Fetcher]) -> None:
        pass
