import logging
from datetime import datetime
from pathlib import Path
from typing import List

from gold import Payment
from gold.fetcher import Fetcher

LOG = logging.getLogger(__name__)

HEADER = [
    "Transaction Date",
    "Transaction Type",
    "Sort Code",
    "Account Number",
    "Transaction Description",
    "Debit Amount",
    "Credit Amount",
    "Balance",
]

FIELD_DATE = HEADER.index("Transaction Date")
FIELD_DESCRIPTION = HEADER.index("Transaction Description")
FIELD_MONEY_IN = HEADER.index("Credit Amount")
FIELD_MONEY_OUT = HEADER.index("Debit Amount")


class Lloyds(Fetcher):
    def __init__(self, csv_directory: Path):
        if not csv_directory.is_dir():
            csv_directory.mkdir(parents=True)
        self.csv_directory = csv_directory

    def fetch(self) -> List[Payment]:
        headers = []
        lines = []
        for csv_file in self.csv_directory.glob("*.csv"):
            with open(str(csv_file), "r") as f:
                headers.append(next(f).strip())
                lines.extend(line.strip().split(",") for line in f)
        LOG.debug("Read %d CSV lines.", len(lines))
        if not lines:
            return []
        assert set(headers) == {",".join(HEADER)}
        assert set(map(len, lines)) == {8}

        return [
            Payment(
                line[FIELD_DESCRIPTION],
                parse_amount_pence(line[FIELD_MONEY_IN], line[FIELD_MONEY_OUT]),
                parse_time(line[FIELD_DATE]),
                None,
                "lloyds",
            )
            for line in lines
        ]


def parse_amount_pence(money_in_str: str, money_out_str: str) -> int:
    if money_in_str:
        return int(money_in_str.replace(".", ""))
    elif money_out_str:
        return -int(money_out_str.replace(".", ""))
    else:
        raise AssertionError()


def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%d/%m/%Y")
