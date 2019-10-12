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


class PaymentModifier(NamedTuple):
    entity: Optional[str] = None
    amount_pence: Optional[int] = None
    time: Optional[datetime] = None
    category: Optional[str] = None
    source: Optional[str] = None

    def modify(self, payment: Payment) -> "Payment":
        if self.entity:
            payment = payment.with_field(entity=self.entity)
        if self.amount_pence:
            payment = payment.with_field(amount_pence=self.amount_pence)
        if self.time:
            payment = payment.with_field(time=self.time)
        if self.category:
            payment = payment.with_field(category=self.category)
        if self.source:
            payment = payment.with_field(source=self.source)
        return payment


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
