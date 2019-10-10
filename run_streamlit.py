from argparse import ArgumentParser
from pathlib import Path

import streamlit as st

from gold import LloydsFetcher, MonzoFetcher


def main():
    parser = ArgumentParser("gold")
    parser.add_argument("--monzo-credentials", type=str, default="secret/monzo.json")
    parser.add_argument("--monzo-cache", type=str, default="secret/monzo-cache.txt")
    parser.add_argument("--lloyds-csv", type=str, default="secret/lloyds")
    args = parser.parse_args()

    payments = get_payments(
        Path(args.lloyds_csv), Path(args.monzo_credentials), Path(args.monzo_cache)
    )
    st.write(payments)


def get_payments(lloyds_csv: Path, monzo_credentials: Path, monzo_cache: Path):
    fetchers = [LloydsFetcher(lloyds_csv), MonzoFetcher(monzo_credentials, monzo_cache)]
    return [payment for fetcher in fetchers for payment in fetcher.fetch()]


if __name__ == "__main__":
    main()
