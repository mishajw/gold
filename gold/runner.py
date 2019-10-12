import pickle
from pathlib import Path
from typing import List

from gold import Payment
from gold.fetcher import Fetcher
from gold.interceptor import Interceptor


def get_payments(
    fetchers: List[Fetcher], interceptors: List[Interceptor], payments_cache: Path
) -> List[Payment]:
    """
    Gets payments from `fetchers` and runs them through `interceptors`.
    """
    if payments_cache.is_file():
        with payments_cache.open("rb") as f:
            payments = pickle.load(f)
    else:
        payments = [payment for fetcher in fetchers for payment in fetcher.fetch()]
    with payments_cache.open("wb") as f:
        pickle.dump(payments, f)

    for interceptor in interceptors:
        payments = interceptor.intercept(payments)
    return payments
