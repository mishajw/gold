from gold import MonzoFetcher, SheetsWriter


def main():
    fetchers = [MonzoFetcher()]
    writer = SheetsWriter()
    writer.write(fetchers)


if __name__ == "__main__":
    main()
