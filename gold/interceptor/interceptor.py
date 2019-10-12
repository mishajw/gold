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


class SingleInterceptor(Interceptor, ABC):
    """
    Modifies payments separately.
    """

    def intercept(self, payments: List[Payment]) -> List[Payment]:
        return list(map(self.intercept_single, payments))

    @abstractmethod
    def intercept_single(self, payment: Payment) -> Payment:
        """
        Replace a single payment with a new payment.
        """
        pass
