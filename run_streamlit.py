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
from gold.payment import PaymentModifier

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
        category=st.selectbox("Category", list(set(p.category for p in payments)))
        if st.checkbox("Filter by category?")
        else None,
    )
    payments = list(filter(payment_specifier.matches, payments))
    assert payments, "No payments matched."

    payments = pd.DataFrame(payments)
    st.write(format_df(payments))

    st.subheader("By date")
    by_time = index(sum_by_column(round_to_period(payments, 7), "time").sort_values("time"), "time")
    st.line_chart(by_time)
    by_time["amount_pence"] = by_time["amount_pence"].cumsum()
    st.line_chart(by_time)

    st.subheader("By entity")
    by_entity = sum_by_column(payments, "entity")
    st.bar_chart(index(by_entity, "entity").sort_values("amount_pence").head(30), height=300)
    st.write(format_df(by_entity))

    st.subheader("By category")
    by_category = sum_by_column(payments, "category")
    st.bar_chart(index(by_category, "category").sort_values("amount_pence"))
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
    return payments.groupby(column)["amount_pence"].sum().sort_values().reset_index()


def index(df: pd.DataFrame, column: str) -> pd.DataFrame:
    return df.rename({column: "index"}, axis=1).set_index("index")


def round_to_period(df: pd.DataFrame, num_days: int) -> pd.DataFrame:
    now_date = datetime.now().date()

    def round_datetime(time: datetime) -> datetime:
        distance_days = (now_date - time.date()).days
        period_start_days_ago = (distance_days // num_days + 1) * num_days
        return datetime.combine(
            now_date - timedelta(days=period_start_days_ago), datetime.min.time()
        )

    df = df.copy()
    df["time"] = df["time"].apply(round_datetime)
    return df


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
