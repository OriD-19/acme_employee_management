from __future__ import annotations
from typing import TYPE_CHECKING
from rich.panel import Panel
from rich.table import Table
from src.menu.pages.screen import Screen

if TYPE_CHECKING:
    from src.menu.app import App

class TransactionScreen(Screen):

    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "employee_transactions"
        self.employees = self.app.employee_store.search_all()

    def render(self):
        console = self.app.console

        console.clear()
        if not self.employees:
            console.print(Panel("[yellow]No employees found.[/]"))
            input("Press ENTER to return...")
            self.app.change_screen("index")
            return

        # List employees
        table = Table(title="Employee Transactions")
        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="cyan")
        table.add_column("Role")

        for i, emp in enumerate(self.employees):
            table.add_row(str(i + 1), emp.name, str(emp.role.name))

        console.print(table)
        console.print("\nSelect an employee to view their transactions (ENTER to cancel):")

    def handle_input(self, user_input: str):
        if not user_input.strip():
            self.app.change_screen("index")
            return

        try:
            index = int(user_input) - 1
            if index < 0 or index >= len(self.employees):
                raise IndexError

            employee = self.employees[index]
            transactions = getattr(employee, "transactions", [])

            self.app.console.clear()
            if not transactions:
                self.app.console.print(Panel(f"[yellow]{employee.name} has no recorded transactions.[/]"))
            else:
                table = Table(title=f"Transactions for {employee.name}")
                table.add_column("#", style="dim", width=4)
                table.add_column("Type", style="green")
                table.add_column("Description")
                table.add_column("Date")

                for i, tx in enumerate(transactions):
                    table.add_row(
                        str(i + 1),
                        tx.get("type", "-"),
                        tx.get("description", "-"),
                        tx.get("timestamp", "-")
                    )

                self.app.console.print(table)

        except (ValueError, IndexError):
            self.app.console.print("[red]Invalid selection.[/]")

        input("\nPress ENTER to return...")
        self.app.change_screen("index")

