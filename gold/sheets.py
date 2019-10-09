from typing import List

from gold import Writer, Fetcher


class SheetsWriter(Writer):
    def write(self, fetcher: List[Fetcher]) -> None:
        raise NotImplementedError()
