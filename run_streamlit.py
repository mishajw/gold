from argparse import ArgumentParser
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

from gold import LloydsFetcher, MonzoFetcher, Payment

TIME_FORMAT = "%Y-%m-%d %H-%M-%S"


parser = ArgumentParser("gold")
parser.add_argument("--monzo-credentials", type=str, default="secret/monzo.json")
parser.add_argument("--monzo-cache", type=str, default="secret/monzo-cache.txt")
parser.add_argument("--lloyds-csv", type=str, default="secret/lloyds")
args = parser.parse_args()


def main():
    payments = payments_to_df(get_payments())
    st.header("Gold")
    st.write(payments)


@st.cache
def get_payments() -> List[Payment]:
    fetchers = [
        LloydsFetcher(Path(args.lloyds_csv)),
        MonzoFetcher(Path(args.monzo_credentials), Path(args.monzo_cache)),
    ]
    return [payment for fetcher in fetchers for payment in fetcher.fetch()]


def payments_to_df(payments: List[Payment]) -> pd.DataFrame:
    payments = pd.DataFrame(payments)
    payments["time"] = payments["time"].map(lambda d: d.strftime(TIME_FORMAT))
    payments["amount"] = payments["amount_pence"].map(lambda p: f"{p / 100:.2f}")
    del payments["amount_pence"]
    payments = payments.sort_values("time", ascending=False)
    return payments


if __name__ == "__main__":
    main()
