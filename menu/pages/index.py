from __future__ import annotations
from menu.pages.screen import Screen
from typing import TYPE_CHECKING
from rich.panel import Panel

if TYPE_CHECKING:
    from menu.app import App


class IndexScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "index"

    def render(self):
        self.app.console.clear()
        self.app.console.print(Panel("Welcome to the Employee Management System"))

        self.app.console.print("1. Create New Employee")
        self.app.console.print("2. List Employees")
        self.app.console.print("3. Freelance Projects")
        self.app.console.print("4. Employee Vacations Request")
        self.app.console.print("5. Payments")
        self.app.console.print("6. Transactions")
        self.app.console.print("7. Exit")

    def handle_input(self, user_input):
        if user_input == "1":
            self.app.change_screen("create_employee")
            return
        elif user_input == "2":
            self.app.change_screen("view_employees")
            return
        elif user_input == "3":
            self.app.change_screen("freelance_projects")
            return
        elif user_input == "4":
            self.app.change_screen("grant_vacations")
            return
        elif user_input == "5":
            self.app.change_screen("pay_employees")
            return
        elif user_input == "6":
            self.app.change_screen("employee_transactions")
            return
        elif user_input == "7":
            self.app.running = False
            self.app.console.print("Bye!")
            return
        else:
            self.app.console.print("[red bold]Insert a valid option[/red bold]")

        self.app.console.input("Press [blue bold]ENTER[/blue bold] to continue...")
