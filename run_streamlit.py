"""
Runs a streamlit UI displaying payment information.
"""
import logging
import pickle
from argparse import ArgumentParser
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

import gold
from gold import Payment, fetcher, interceptor

TIME_FORMAT = "%Y-%m-%d %H-%M-%S"

parser = ArgumentParser("gold")
parser.add_argument("--payments-cache", type=str, default="secret/payments-cache")
parser.add_argument("--monzo-credentials", type=str, default="secret/monzo.json")
parser.add_argument("--monzo-cache", type=str, default="secret/monzo-cache")
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


def get_payments() -> List[Payment]:
    return gold.get_payments(
        [
            fetcher.Lloyds(Path(args.lloyds_csv)),
            fetcher.Monzo(Path(args.monzo_credentials), Path(args.monzo_cache)),
        ],
        [interceptor.Rename("E KNIGHT", "EMMA KNIGHT")],
        Path(args.payments_cache)
    )


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
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
