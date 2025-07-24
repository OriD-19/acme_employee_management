from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
 
if TYPE_CHECKING:
    from src.employee.employee import Employee, EmployeeRoles
    from src.employee.payment import PaymentMethod


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> bool:
        pass


class AbstractVacationHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(
        self, request: tuple[Employee, bool, int]
    ):  # the request type of the handle will be an employee
        if self._next_handler:
            return self._next_handler.handle(request)

        # if the whole request was validated successfully
        return True

class AbstractPaymentHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler
    
    @abstractmethod
    def handle(self, request: tuple[PaymentMethod, EmployeeRoles]) -> Optional[float]:
        """
        Returns a tuple containing the elements:
        1. Payment
        2. Has Bonus
        3. Bonus quantity
        """
        if self._next_handler:
            return self._next_handler.handle(request)
        
        return None