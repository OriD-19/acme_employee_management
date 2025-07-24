from __future__ import annotations
from typing import TYPE_CHECKING
from rich.panel import Panel
from rich.table import Table
from rich.console import Console
from src.menu.pages.screen import Screen
from src.logs.events import Events

if TYPE_CHECKING:
    from src.menu.app import App


class PaymentScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "pay_employees"

    def render(self):
        console: Console = self.app.console
        employees = self.app.employee_store.search_all()
        console.clear()

        if not employees:
            console.print(Panel("[yellow]No employees found.[/]"))
            input("Press ENTER to return...")
            self.app.change_screen("index")
            return

        console.print(
            Panel("[bold green]Employee Payment Summary[/]", border_style="green")
        )

        for emp in employees:
            table = Table.grid(padding=(0, 2))
            table.add_column(style="dim")
            table.add_column()

            table.add_row("Name", emp.name)
            table.add_row(
                "Role", str(emp.role.name if hasattr(emp.role, "name") else emp.role)
            )
            table.add_row(
                "Payment Type",
                emp.payment_method.type_name
                if hasattr(emp.payment_method, "type_name")
                else type(emp.payment_method).__name__,
            )

            # Add strategy-specific info
            pm = emp.payment_method

            amount = self.app.payment_service.make_payment(emp, pm)
            bonus = self.app.payment_service.get_bonus(pm, emp.role)

            required_fields = pm.required_fields()

            for field in required_fields:
                field_name = field[0]
                field_name.replace("_", " ")
                field_name.capitalize()
                val = getattr(pm, field[0], "...")
                table.add_row(
                    field_name,
                    f"{'$' if field[2] is float else ''}{len(val) if isinstance(val, list) else val}",
                )

            if bonus:
                table.add_row("[bold green]Bonus[/bold green]", f"${bonus:.2f}")
                amount += bonus

            table.add_row("[bold blue]Total[/bold blue]", f"${amount:.2f}")

            self.app.event_manager.notify(
                Events.PAYMENT_EVENT,
                {
                    "event_type": Events.PAYMENT_EVENT.value,
                    "description": f"Paid ${amount:.2f}",
                    "employee": emp,
                    "total_paid": amount,
                },
            )

            if bonus:
                self.app.event_manager.notify(
                    Events.BONUS_PAYMENT_EVENT,
                    {
                        "event_type": Events.BONUS_PAYMENT_EVENT.value,
                        "employee": emp,
                        "description": f"Applicable for bonus of ${bonus:.2f}",
                        "bonus": bonus,
                    },
                )

            console.print(Panel(table, border_style="cyan"))

        console.print("Press [bold blue]ENTER[/bold blue] to go back...")

    def handle_input(self, user_input: str):
        # No interactive input expected during render
        self.app.change_screen("index")
