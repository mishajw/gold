from gold import Payment
from gold.interceptor import MapInterceptor


class Rename(MapInterceptor):
    """
    Renames a payment's entity.
    """

    def __init__(self, from_entity: str, to_entity: str):
        self.from_entity = from_entity
        self.to_entity = to_entity

    def map(self, payment: Payment) -> Payment:
        if payment.entity == self.from_entity:
            return payment.with_field(entity=self.to_entity)
        return payment
