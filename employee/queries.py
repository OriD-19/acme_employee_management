from employee.roles import EmployeeRoles
from employee.employee import Employee
from abc import ABC, abstractmethod

class SingletonMeta(type):
    """Singleton class for instantiating just one store through the whole system"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]

class EmployeeStore(ABC):
    """Interface for defining methods that all the Query objects must implement to interact with the client"""

    @abstractmethod
    def search_all(self) -> list[Employee]: ...

    @abstractmethod
    def search_by_role(self, role: EmployeeRoles) -> list[Employee]: ...

    @abstractmethod
    def add_employee(self, employee: Employee) -> None: ...


class EmployeeInMemoryStore(EmployeeStore):
    """Representation for the InMemory strategy for the Employee QueryObject"""

    def __init__(self, store: list[Employee]):
        self.store = store

    def search_all(self) -> list[Employee]:
        return self.store

    def search_by_role(self, role: EmployeeRoles) -> list[Employee]:
        return [employee for employee in self.store if employee.role == role]
    
    def add_employee(self, employee: Employee) -> None:
        self.store.append(employee)
