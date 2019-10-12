from gold import Payment
from gold.interceptor import SingleInterceptor


class Rename(SingleInterceptor):
    """
    Renames a payment's entity.
    """

    def __init__(self, from_entity: str, to_entity: str):
        self.from_entity = from_entity
        self.to_entity = to_entity

    def intercept_single(self, payment: Payment) -> Payment:
        print(payment)
        if payment.entity == self.from_entity:
            return payment.with_field(entity=self.to_entity)
        return payment
