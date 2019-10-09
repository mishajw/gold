import json
import logging
from pathlib import Path
from typing import List

from pymonzo import MonzoAPI

from gold import Fetcher, Payment

LOG = logging.getLogger(__name__)

AUTH_CODE_URL_TEMPLATE = (
    "https://auth.monzo.com/"
    "?response_type=code"
    "&redirect_uri=https://github.com/pawelad/pymonzo"
    "&client_id={}"
)


class MonzoFetcher(Fetcher):
    def __init__(self, credentials_file: Path, auth_code_output_file: Path):
        self.credentials_file = credentials_file
        self.auth_code_output_file = auth_code_output_file

    def fetch(self) -> List[Payment]:
        api = self.__get_api()
        account = api.accounts()[0]
        LOG.debug("Fetched account: %s", account)
        transactions = api.transactions(account)
        LOG.debug("Fetched %d transactions: %s", len(transactions), transactions)
        raise NotImplementedError()

    def __get_api(self) -> MonzoAPI:
        with open(str(self.credentials_file), "r") as f:
            credentials = json.load(f)

        if "access_token" in credentials:
            return MonzoAPI(access_token=credentials["access_token"])

        # TODO: Check this works.
        assert "client_id" in credentials, "Can't find ID in credentials."
        assert "client_secret" in credentials, "Can't find secret in credentials."

        auth_code_url = AUTH_CODE_URL_TEMPLATE.format(credentials["client_id"])
        print(f"Go to {auth_code_url} and paste the response here.")
        auth_code = input("Response: ").strip()

        LOG.debug("Creating Monzo API")
        return MonzoAPI(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            auth_code=auth_code,
        )
