"""
Runs a streamlit UI displaying payment information.
"""

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
    payments = pd.DataFrame(get_payments())
    by_entity = sum_by_column(payments, "entity")
    by_category = sum_by_column(payments, "category")

    st.header("Gold")
    st.subheader("By date")
    st.write(format_df(payments))
    st.subheader("By entity")
    st.write(format_df(by_entity))
    st.subheader("By category")
    st.write(format_df(by_category))


@st.cache
def get_payments() -> List[Payment]:
    fetchers = [
        LloydsFetcher(Path(args.lloyds_csv)),
        MonzoFetcher(Path(args.monzo_credentials), Path(args.monzo_cache)),
    ]
    return [payment for fetcher in fetchers for payment in fetcher.fetch()]


def sum_by_column(payments: pd.DataFrame, column: str) -> pd.DataFrame:
    return payments.groupby(column)["amount_pence"].sum().sort_values(ascending=False).to_frame()


def format_df(payments: pd.DataFrame) -> pd.DataFrame:
    if "amount_pence" in payments:
        payments["amount"] = payments["amount_pence"].map(lambda p: f"{p / 100:.2f}")
        del payments["amount_pence"]
    if "time" in payments:
        payments["time"] = payments["time"].map(lambda d: d.strftime(TIME_FORMAT))
        payments = payments.sort_values("time", ascending=False)
    return payments


if __name__ == "__main__":
    main()
