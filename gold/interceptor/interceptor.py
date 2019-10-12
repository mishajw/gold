from abc import ABC, abstractmethod
from typing import List

from gold import Payment


class Interceptor(ABC):
    """
    Modifies payments.
    """

    @abstractmethod
    def intercept(self, payments: List[Payment]) -> List[Payment]:
        """
        Replace a list of payments with a new list of payments.
        """
        pass


class MapInterceptor(Interceptor, ABC):
    """
    Modifies payments separately.
    """

    def intercept(self, payments: List[Payment]) -> List[Payment]:
        return list(map(self.map, payments))

    @abstractmethod
    def map(self, payment: Payment) -> Payment:
        """
        Replace a single payment with a new payment.
        """
        pass


class FlatMapInterceptor(Interceptor, ABC):
    """
    Modifies payments separately.
    """

    def intercept(self, payments: List[Payment]) -> List[Payment]:
        return [intercepted for payment in payments for intercepted in self.flat_map(payment)]

    @abstractmethod
    def flat_map(self, payment: Payment) -> List[Payment]:
        """
        Replace a single payment with a new payment.
        """
        pass
