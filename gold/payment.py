from datetime import datetime
from typing import NamedTuple, Optional


class Payment(NamedTuple):
    entity: str
    amount_pence: int
    time: datetime
    category: Optional[str]
    source: str

    def with_field(self, **kwargs) -> "Payment":
        return self._replace(**kwargs)
