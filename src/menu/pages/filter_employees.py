from __future__ import annotations
from typing import TYPE_CHECKING
from rich.panel import Panel
from src.employee.roles import EmployeeRoles
from src.menu.pages.components.components import EmployeeTable
from src.menu.pages.screen import Screen

if TYPE_CHECKING:
    from src.menu.app import App


class FilterEmployeesScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "view_employees"

    def render(self):
        self.app.console.clear()
        self.app.console.print(Panel("List employees"))

        self.app.console.print("1. List all employees")
        self.app.console.print("2. Filter by Interns")
        self.app.console.print("3. Filter by Managers")
        self.app.console.print("4. Filter by Vice Presidents")
        self.app.console.print("5. Back to main menu")

    def handle_input(self, user_input):
        table = EmployeeTable()

        if user_input == "1":
            table.add_info(self.app.employee_store.search_all()).render()
        elif user_input == "2":
            table.add_info(self.app.employee_store.search_by_role(EmployeeRoles.INTERN)).render()
        elif user_input == "3":
            table.add_info(self.app.employee_store.search_by_role(EmployeeRoles.MANAGER)).render()
        elif user_input == "4":
            table.add_info(
                self.app.employee_store.search_by_role(EmployeeRoles.VICE_PRESIDENT)
            ).render()
        elif user_input == "5":
            # go back to the index page
            self.app.change_screen("index")
            return

        self.app.console.input("Press [blue bold]ENTER[/blue bold] to continue...")
