"""
Runs a streamlit UI displaying payment information.
"""
import logging
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

import gold
from gold import Payment, fetcher, interceptor, PaymentSpecifier

TIME_FORMAT = "%Y-%m-%d %H-%M-%S"

parser = ArgumentParser("gold")
parser.add_argument("--payments-cache", type=str, default="secret/payments-cache")
parser.add_argument("--monzo-credentials", type=str, default="secret/monzo.json")
parser.add_argument("--monzo-cache", type=str, default="secret/monzo-cache")
parser.add_argument("--lloyds-csv", type=str, default="secret/lloyds")
args = parser.parse_args()


def main():
    st.header("Gold")

    payments = get_payments()
    payment_specifier = PaymentSpecifier(
        entity_regex=st.text_input("Entity regex:", ".*"),
        time_min=datetime.combine(
            st.date_input("From:", datetime.now() - timedelta(weeks=20)), datetime.min.time()
        ),
        time_max=datetime.combine(st.date_input("To:", datetime.now()), datetime.min.time()),
    )
    payments = list(filter(payment_specifier.matches, payments))
    assert payments, "No payments matched."

    payments = pd.DataFrame(payments)
    by_entity = sum_by_column(payments, "entity")
    by_category = sum_by_column(payments, "category")

    st.subheader("By date")
    st.write(format_df(payments))
    st.subheader("By entity")
    bar_chart(by_entity, "entity")
    st.write(format_df(by_entity))
    st.subheader("By category")
    bar_chart(by_category, "category")
    st.write(format_df(by_category))


def get_payments() -> List[Payment]:
    return gold.get_payments(
        [
            # TODO: Add fetchers for your payments.
        ],
        [
            # TODO: Add interceptors for your payments.
        ],
        Path(args.payments_cache),
    )


def sum_by_column(payments: pd.DataFrame, column: str) -> pd.DataFrame:
    return payments.groupby(column)["amount_pence"].sum().sort_values(ascending=False).reset_index()


def bar_chart(df: pd.DataFrame, column: str) -> None:
    st.bar_chart(
        df.rename({column: "index"}, axis=1)
        .set_index("index")
        .sort_values("amount_pence")
        .head(10),
        height=300,
    )


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
