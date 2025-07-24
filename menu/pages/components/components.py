from abc import ABC, abstractmethod
from collections.abc import Iterable
from rich.table import Table as RichTable
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from employee.employee import Employee
from typing import Any


class Component(ABC):
    data: Any = None
    console: Console = Console()

    @abstractmethod
    def render(self): ...


class EmployeeTable(Component):
    def __init__(self):
        self.table = RichTable()
        self.console = Console()

        self.table.add_column("Name")
        self.table.add_column("Role")
        self.table.add_column("Empl. Type")
        self.table.add_column("Date added")

    def add_info(self, data: Iterable[Employee], filter_by_role: str = ""):
        self.table.title = "Employees" + (
            f" (filtered by {filter_by_role})" if filter_by_role else ""
        )

        for employee in data:
            self.table.add_row(
                employee.name,
                employee.role.value,
                str(employee.payment_method),
                employee.date_joined.strftime("%Y-%m-%d"),
            )

        return self

    def render(self):
        self.console.print(self.table)


class ConfirmationMessageComponent(Component):
    def render(self, message: str, prompt: str = "Press ENTER to continue"):
        panel_text = Text()
        panel_text.append(message + "\n\n", style="bold green")
        panel_text.append(prompt, style="dim")

        self.console.clear()
        self.console.print(
            Panel(panel_text, title="✅ Confirmation", border_style="green")
        )
        input()


class EmployeeSummaryComponent(Component):
    def render(self, employee: Employee):
        table = RichTable(show_header=False, show_lines=False, padding=(0, 1))

        # General Info
        table.add_row("Name", employee.name)
        table.add_row(
            "Role",
            str(
                employee.role.name if hasattr(employee.role, "name") else employee.role
            ),
        )
        table.add_row("Joined", employee.date_joined.strftime("%Y-%m-%d"))
        table.add_row("Vacation Days", str(employee.vacation_days))

        # Payment Info
        payment = employee.payment_method
        if hasattr(payment, "__dict__"):
            for key, value in payment.__dict__.items():
                table.add_row(key.replace("_", " ").title(), str(value))

        panel = Panel(
            table, title="Employee Summary", border_style="cyan", padding=(1, 2)
        )
        self.console.clear()
        self.console.print(panel)
        self.console.print("\n[dim]Press ENTER to return to main menu...[/]")
        input()
