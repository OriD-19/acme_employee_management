from abc import ABC, abstractmethod
from enum import Enum
from src.general.cor_handlers import AbstractPaymentHandler
from src.employee.roles import EmployeeRoles
from typing import TypedDict
from src.config.config import config


class PaymentMethods(Enum):
    SALARIED_PAYMENT = "salaried"
    HOURLY_PAYMENT = "hourly"
    PER_PROJECT_PAYMENT = "freelance"


class FreelanceProjectFormat(TypedDict):
    name: str
    payment: float


class PaymentMethod(ABC):
    """Interface for choosing a strategy to pay the employee according to its type"""

    type_name: str

    @classmethod
    def required_fields(cls) -> list[tuple[str, str, type]]:
        return []

    @abstractmethod
    def pay(self, employee) -> float: ...


class HourlyPayment(PaymentMethod):
    type_name = "hourly"

    def __init__(self, hours: int, rate: float):
        self.hours: int = hours
        self.rate: float = rate

    @classmethod
    def required_fields(cls):
        return [
            ("hours", "Hours Worked:", int),
            ("rate", "Hourly Rate:", float),
        ]

    def pay(self, employee):
        return self.hours * self.rate

    def __str__(self):
        return "Hourly"


class SalariedPayment(PaymentMethod):
    type_name = "salaried"

    def __init__(self, salary: float):
        self.salary: float = salary

    @classmethod
    def required_fields(cls):
        return [("salary", "Monthly Salary (USD):", float)]

    def pay(self, employee):
        return self.salary

    def __str__(self):
        return "Salaried"


# for Freelancers
class FreelancePayment(PaymentMethod):
    type_name = "freelance"
    projects: list[FreelanceProjectFormat]

    def __init__(self, pay_per_project: float):
        self.pay_per_project = pay_per_project
        self.projects = []

    @classmethod
    def required_fields(cls):
        return [
            ("projects", "Number of Projects:", list),
            ("pay_per_project", "Payment per Project:", float),
        ]

    def pay(self, employee):
        sum = 0

        for proj in self.projects:
            sum += proj["payment"]

        return sum

    def __str__(self):
        return "Freelancer"


# Chain of responsibility for bonuses
# TODO add configuration support for all the values defined in here


class InternBonusHandler(AbstractPaymentHandler):
    def handle(self, request):
        role = request[1]

        if role == EmployeeRoles.INTERN:
            return None  # stop processing right away

        return super().handle(request)


class SalariedBonusHandler(AbstractPaymentHandler):
    def handle(self, request):
        method = request[0]

        salaried_bonus_percentage = config.get("salaryBonusPercentage")
        if method.type_name == "salaried":
            return method.salary * salaried_bonus_percentage

        return super().handle(request)


class HourlyBonusHandler(AbstractPaymentHandler):
    def handle(self, request):
        method = request[0]

        min_hours_for_bonus = config.get("minHoursForHourlyBonus")
        if method.type_name == "hourly":
            if method.hours > min_hours_for_bonus:
                return 100

        return super().handle(request)


class PaymentService:
    def make_payment(self, employee, payment_method: PaymentMethod):
        return payment_method.pay(employee)

    def get_bonus(self, payment_method: PaymentMethod, employee_role: EmployeeRoles):
        handlers: list[AbstractPaymentHandler] = [
            InternBonusHandler(),
            SalariedBonusHandler(),
            HourlyBonusHandler(),
        ]

        initial_handler = handlers[0]

        for i in range(len(handlers) - 1):
            handlers[i].set_next(handlers[i + 1])

        return initial_handler.handle((payment_method, employee_role))
