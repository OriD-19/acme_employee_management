from __future__ import annotations
from typing import TYPE_CHECKING
from rich.panel import Panel
from rich.table import Table
from src.menu.pages.screen import Screen
from rich.prompt import Confirm
from src.logs.events import Events

if TYPE_CHECKING:
    from src.menu.app import App


class VacationGrantScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "grant_vacations"
        self._employees = self.app.employee_store.search_all()

    def render(self):
        console = self.app.console

        console.clear()
        if not self._employees:
            console.print(Panel("[yellow]No employees found.[/]"))
            input("Press ENTER to return...")
            self.app.change_screen("index")
            return

        table = Table(title="Grant Vacation Days")
        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="cyan")
        table.add_column("Role")
        table.add_column("Available Vacation Days", justify="center")

        for i, emp in enumerate(self._employees):
            table.add_row(
                str(i + 1), emp.name, str(emp.role.name), str(emp.vacation_days)
            )

        console.print(table)
        console.print("\nSelect an employee by number (or press ENTER to cancel):")

    def handle_input(self, user_input: str):
        if not user_input.strip():
            self.app.change_screen("index")
            return

        try:
            index = int(user_input) - 1
            if index < 0 or index >= len(self._employees):
                raise IndexError

            employee = self._employees[index]

            wants_payout = Confirm.ask("Do you want to request payout during vacation?")
            days = input("How many vacation days to grant? ")

            try:
                days = int(days)

                # perform validation logic with Chain of Responsibility
                valid_request = self.app.vacation_service.validate(
                    (employee, wants_payout, days)
                )

                if not valid_request:
                    self.app.console.print(
                        Panel(
                            f"[red]Request Denied. Does not meet the policies.\nDays: {days}\nPayout: {'Yes' if wants_payout else 'No'}[/]",
                            title="✅ Denied",
                            border_style="red",
                        )
                    )
                    input("Press ENTER to return...")
                    self.app.change_screen("index")
                    return

                employee.vacation_days -= days
                self.app.console.print(
                    Panel(
                        f"[green]Vacation granted for {employee.name}.\nDays: {days}\nPayout: {'Yes' if wants_payout else 'No'}[/]",
                        title="✅ Success",
                        border_style="green",
                    )
                )

                self.app.event_manager.notify(Events.VACATION_EVENT, {
                    "event_type": Events.VACATION_EVENT.value,
                    "description": f"Granted {days} of vacation {"with" if wants_payout else "without"} payout",
                    "employee": employee,
                    "days": days,
                    "payout": wants_payout
                })

            except ValueError:
                self.app.console.print("[red]Invalid number of days.[/]")

        except (ValueError, IndexError):
            self.app.console.print("[red]Invalid selection.[/]")

        input("Press ENTER to return...")
        self.app.change_screen("index")
