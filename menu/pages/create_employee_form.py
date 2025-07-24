from rich.panel import Panel
from menu.pages.screen import Screen
from employee.employee import EmployeeBuilder
from employee.roles import EmployeeRoles
from employee.payment import PaymentMethod
from menu.pages.components.components import ConfirmationMessageComponent, EmployeeSummaryComponent


class CreateEmployeeScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.view_name = "create_employee"
        self.payment_types = self._get_payment_type_map()
        self.steps = self._build_steps()
        self.step_index = 0
        self.responses = {}
        self.employee = None
        self.branched = False

    def _reset(self):
        self.steps = self._build_steps()
        self.step_index = 0
        self.responses = {}
        self.employee = None
        self.branched = False

    def _get_payment_type_map(self):
        return {cls.type_name: cls for cls in PaymentMethod.__subclasses__()}

    def _build_steps(self):
        employee_type_options = ", ".join(self.payment_types.keys())
        return [
            ("name", "Enter employee name:", str),
            (
                "role",
                f"Enter role ({', '.join([r.name for r in EmployeeRoles])}):",
                EmployeeRoles,
            ),
            ("type", f"Enter employee type ({employee_type_options}):", str),
        ]

    def render(self):
        self.app.console.clear()
        if self.step_index < len(self.steps):
            key, prompt, _ = self.steps[self.step_index]
            self.app.console.print("steps: ", len(self.steps))
            self.app.console.print(Panel(f"[bold]{prompt}[/]"))
        else:
            ConfirmationMessageComponent().render("Employee Created Successfully!")

    def handle_input(self, user_input):
        if self.step_index < len(self.steps):
            key, _, expected_type = self.steps[self.step_index]
            value = user_input.strip()

            if not value:
                self.app.console.print("[red]Input cannot be empty.[/]")
                return

            try:
                if expected_type == EmployeeRoles:
                    value = EmployeeRoles[value.upper()]
                elif expected_type is str:
                    value = value.lower() if key == "type" else value

                if key == "type" and value not in self.payment_types:
                    raise ValueError(f"Unknown employee type: {value}")

                self.responses[key] = value
                self.step_index += 1

                if self.step_index == len(self.steps) and not self.branched:
                    # Add branching based on type
                    self.branched = True
                    self._branch_steps()

            except Exception as e:
                self.app.console.print(f"[red]Invalid input: {e}[/]")
        else:
            self._create_employee()
            self._reset()
            self.app.change_screen("index")

    def _branch_steps(self):
        emp_type = self.responses["type"]
        payment_class = self.payment_types[emp_type]
        self.steps.extend([field for field in payment_class.required_fields() if field[2] is not list])

    def _create_employee(self):
        builder = EmployeeBuilder()
        builder.set_name(self.responses["name"])
        builder.set_role(self.responses["role"])
        builder.set_vacation_days(15)

        emp_type = self.responses["type"]
        payment_class = self.payment_types[emp_type]

        # Extract only the required field names
        payment_kwargs = {}
        for field in payment_class.required_fields():
            if field[2] is list:
                continue

            val = None
            if field[2] is int:
                val = int(self.responses[field[0]])
            elif field[2] is float:
                val = float(self.responses[field[0]])
            elif field[2] is str:
                pass
            else:
                raise ValueError("Could not parse the value into any of the valid datatypes")

            payment_kwargs[field[0]] = val

        payment = payment_class(**payment_kwargs)

        builder.set_payment_strategy(payment)
        self.employee = builder.get_employee()
        self.app.employee_store.add_employee(self.employee)
        EmployeeSummaryComponent().render(self.employee)