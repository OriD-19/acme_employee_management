from __future__ import annotations
from src.employee.employee import EmployeeRoles, Employee
from src.general.cor_handlers import AbstractVacationHandler

FIXED_PAYOUT_VACATION_DAYS = 5


class GeneralVacationHandler(AbstractVacationHandler):
    def handle(self, request):
        employee, payout, days_requested = request

        if payout and employee.vacation_days < FIXED_PAYOUT_VACATION_DAYS:
            return False

        # pass it to the next handler in the chain
        return super().handle(request)


class InternVacationHandler(AbstractVacationHandler):
    def handle(self, request):
        employee, _, _ = request

        if employee.role == EmployeeRoles.INTERN:
            return False  # Do not process the request any further

        return super().handle(request)


class ManagerVacationHandler(AbstractVacationHandler):
    def handle(self, request):
        employee, payout, days_requested = request

        # only manager employees
        if employee.role != EmployeeRoles.MANAGER:
            return super().handle(request)

        if employee.vacation_days - days_requested < 0:
            return False

        if payout:
            # request payout vacation for a max of 10 days
            if days_requested > 10:
                return False

        return super().handle(request)


class VicePresidentVacationHandler(AbstractVacationHandler):
    def handle(self, request):
        employee, payout, days_requested = request

        if employee.role != EmployeeRoles.VICE_PRESIDENT:
            return super().handle(request)

        if days_requested > 5:
            return False

        return super().handle(request)


class VacationService:
    def __init__(self):
        self.handlers: list[AbstractVacationHandler] = [
            GeneralVacationHandler(),
            InternVacationHandler(),
            ManagerVacationHandler(),
            VicePresidentVacationHandler(),
        ]

    def validate(self, payload: tuple[Employee, bool, int]):

        initial_handler = self.handlers[0]

        for i in range(len(self.handlers) - 1):
            self.handlers[i].set_next(self.handlers[i+1])

        return initial_handler.handle(payload)
