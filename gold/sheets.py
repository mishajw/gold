from typing import List

from gold import Writer, Fetcher


class SheetsWriter(Writer):
    def write(self, fetchers: List[Fetcher]) -> None:
        for fetcher in fetchers:
            for payment in fetcher.fetch():
                print(payment)

        raise NotImplementedError()
