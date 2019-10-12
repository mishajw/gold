import re
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


class PaymentSpecifier(NamedTuple):
    entity_regex: Optional[str] = None
    amount_pence_min: Optional[int] = None
    amount_pence_max: Optional[int] = None
    time_min: Optional[datetime] = None
    time_max: Optional[datetime] = None
    category: Optional[str] = None
    source: Optional[str] = None

    def matches(self, payment: Payment) -> bool:
        matches = True
        if self.entity_regex:
            matches = matches and re.match(self.entity_regex, payment.entity)
        if self.amount_pence_min:
            matches = matches and payment.amount_pence >= self.amount_pence_min
        if self.amount_pence_max:
            matches = matches and payment.amount_pence <= self.amount_pence_max
        if self.time_min:
            matches = matches and payment.time >= self.time_min
        if self.time_max:
            matches = matches and payment.time <= self.time_max
        if self.category:
            matches = matches and payment.category == self.category
        if self.source:
            matches = matches and payment.source == self.source
        return matches
