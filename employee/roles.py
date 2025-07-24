from enum import Enum

class EmployeeRoles(Enum):
    INTERN = "Intern"
    MANAGER = "Manager"
    VICE_PRESIDENT = "Vice President"

    def __str__(self):
        return self.value 