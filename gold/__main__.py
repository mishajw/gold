import logging
from argparse import ArgumentParser
from pathlib import Path

from gold import MonzoFetcher, SheetsWriter, LloydsFetcher


def main():
    parser = ArgumentParser("gold")
    parser.add_argument("--monzo-credentials", type=str, default="secret/monzo.json")
    parser.add_argument("--monzo-cache", type=str, default="secret/monzo-cache.txt")
    parser.add_argument("--lloyds-csv", type=str, default="secret/lloyds")
    args = parser.parse_args()

    fetchers = [
        LloydsFetcher(Path(args.lloyds_csv)),
        MonzoFetcher(Path(args.monzo_credentials), Path(args.monzo_cache)),
    ]
    writer = SheetsWriter()
    writer.write(fetchers)


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
