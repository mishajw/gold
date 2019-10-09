from typing import NamedTuple


class Payment(NamedTuple):
    entity: str
    amount_pence: int
