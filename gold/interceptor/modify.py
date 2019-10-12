from gold import Payment
from gold.interceptor import MapInterceptor
from gold.payment import PaymentModifier, PaymentSpecifier


class Modify(MapInterceptor):
    """
    Modifies a payment's entity.
    """

    def __init__(self, specifier: PaymentSpecifier, modifier: PaymentModifier):
        self.specifier = specifier
        self.modifier = modifier

    def map(self, payment: Payment) -> Payment:
        if not self.specifier.matches(payment):
            return payment
        return self.modifier.modify(payment)
