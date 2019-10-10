import json
import logging
from pathlib import Path
from typing import List

from libmonzo import MonzoClient

from gold import Fetcher, Payment

LOG = logging.getLogger(__name__)

AUTH_CODE_URL_TEMPLATE = (
    "https://auth.monzo.com/"
    "?response_type=code"
    "&redirect_uri=https://github.com/pawelad/pymonzo"
    "&client_id={}"
)


class MonzoFetcher(Fetcher):
    def __init__(self, credentials_file: Path, access_token_cache_file: Path):
        self.credentials_file = credentials_file
        self.access_token_cache_file = access_token_cache_file

    def fetch(self) -> List[Payment]:
        api = self.__get_api()
        account = api.accounts()[0]
        LOG.debug("Fetched account: %s", account)
        transactions = api.transactions(account_id=account.identifier)
        LOG.debug("Fetched %d transactions: %s", len(transactions), transactions)
        raise NotImplementedError()

    def __get_api(self) -> MonzoClient:
        with open(str(self.credentials_file), "r") as f:
            credentials = json.load(f)
        assert "client_id" in credentials, "Can't find client_id in credentials."
        assert "owner_id" in credentials, "Can't find owner_id in credentials."
        assert "client_secret" in credentials, "Can't find client_secret in credentials."

        client = MonzoClient(
            client_id=credentials["client_id"],
            owner_id=credentials["owner_id"],
            client_secret=credentials["client_secret"],
        )

        if self.access_token_cache_file.is_file():
            access_token = self.access_token_cache_file.read_text().strip()
            client.access_token = access_token
        else:
            assert client.authenticate()
            self.access_token_cache_file.write_text(client.access_token)
        return client
