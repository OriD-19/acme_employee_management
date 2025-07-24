from src.employee.payment import PaymentMethod
from src.employee.roles import EmployeeRoles
from datetime import datetime
from typing import TypedDict


class TransactionFormat(TypedDict):
    type: str
    description: str
    timestamp: str


class Employee:
    name: str
    role: EmployeeRoles
    vacation_days: int
    payment_method: PaymentMethod
    date_joined: datetime
    # transactions have default values that are always present
    transactions: list[TransactionFormat]

    def __str__(self):
        return f"{self.name} - {self.role}"


class EmployeeBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.employee = Employee()

    def set_name(self, name: str):
        self.employee.name = name
        return self

    def set_role(self, role: EmployeeRoles):
        self.employee.role = role
        return self

    def set_vacation_days(self, vacation_days: int):
        self.employee.vacation_days = vacation_days
        return self

    def set_payment_strategy(self, payment_method: PaymentMethod):
        self.employee.payment_method = payment_method
        return self

    def get_employee(self) -> Employee:
        empl = self.employee
        self.reset()
        empl.date_joined = datetime.now()
        return empl
