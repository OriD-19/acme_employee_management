from employee.employee import Employee

import random
from employee.employee import EmployeeBuilder
from employee.roles import EmployeeRoles
from employee.payment import SalariedPayment, HourlyPayment, FreelancePayment


def generate_mock_employee():
    names = ["Alice", "Bob", "Carlos", "Diana", "Eva", "Frank"]
    roles = list(EmployeeRoles)

    name = random.choice(names)
    role = random.choice(roles)
    vacation_days = random.randint(5, 30)

    payment_type = random.choice(["salaried", "hourly", "freelance"])
    if payment_type == "salaried":
        payment = SalariedPayment(salary=random.randint(2000, 7000))
    elif payment_type == "hourly":
        payment = HourlyPayment(
            hours=random.randint(20, 160), rate=random.randint(15, 50)
        )
    else:
        payment = FreelancePayment(
            pay_per_project=random.randint(300, 1500),
        )

    builder = EmployeeBuilder()
    return (
        builder.set_name(name)
        .set_role(role)
        .set_vacation_days(vacation_days)
        .set_payment_strategy(payment)
        .get_employee()
    )


store: list[Employee] = [generate_mock_employee() for _ in range(10)]
