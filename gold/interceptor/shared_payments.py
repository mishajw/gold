from datetime import timedelta
from typing import List

from gold import Payment, PaymentSpecifier
from gold.interceptor import FlatMapInterceptor


class SharedPayments(FlatMapInterceptor):
    def __init__(
        self,
        payment_specifier: PaymentSpecifier,
        entities: List[str],
        payment_leniency: timedelta = timedelta(days=7),
    ):
        self.payment_specifier = payment_specifier
        self.entities = entities
        self.payment_leniency = payment_leniency

    def flat_map(self, payment: Payment) -> List[Payment]:
        if not self.payment_specifier.matches(payment):
            return [payment]

        amount_per_person_pence = payment.amount_pence // (1 + len(self.entities))
        new_payment = payment.with_field(amount_pence=amount_per_person_pence)
        entity_payments = [
            payment.with_field(entity=entity, amount_pence=amount_per_person_pence, category="lend")
            for entity in self.entities
        ]
        return [new_payment] + entity_payments
