from __future__ import annotations
from typing import TYPE_CHECKING
from rich.panel import Panel
from rich.table import Table
from src.menu.pages.screen import Screen

if TYPE_CHECKING:
    from src.menu.pages.screen import App


class FreelanceProjectsScreen(Screen):
    def __init__(self, app: App):
        super().__init__(app)
        self.view_name = "freelance_projects"

    def render(self):
        console = self.app.console
        freelancers = [
            e
            for e in self.app.employee_store.search_all()
            if hasattr(e.payment_method, "type_name")
            and e.payment_method.type_name == "freelance"
        ]

        console.clear()
        if not freelancers:
            console.print(Panel("[yellow]No freelance employees found.[/]"))
            input("Press ENTER to return...")
            self.app.change_screen("index")
            return

        # List freelancers
        table = Table(title="👷 Freelance Collaborators")
        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="cyan")
        table.add_column("Projects", justify="center")

        for i, f in enumerate(freelancers):
            project_count = len(getattr(f.payment_method, "projects", []))
            table.add_row(str(i + 1), f.name, str(project_count))

        console.print(table)
        console.print("\nSelect a freelancer to add a project (ENTER to cancel):")

        self.freelancers = freelancers

    def handle_input(self, user_input: str):
        if not user_input.strip():
            self.app.change_screen("index")
            return

        try:
            idx = int(user_input) - 1
            freelancer = self.freelancers[idx]

            name = input("Project name: ").strip()
            payment = float(input("Payment amount: ").strip())

            if not hasattr(freelancer.payment_method, "projects"):
                freelancer.payment_method.projects = []

            freelancer.payment_method.projects.append(
                {"name": name, "payment": payment}
            )

            self.app.console.print(
                Panel(
                    f"[green]Project added for {freelancer.name}:[/]\n• {name} - ${payment:.2f}",
                    title="✅ Success",
                    border_style="green",
                )
            )

        except (IndexError, ValueError):
            self.app.console.print("[red]Invalid input.[/]")

        table = Table(title=f"Projects for {freelancer.name}")
        table.add_column("Name")
        table.add_column("Payment")
        for proj in freelancer.payment_method.projects:
            table.add_row(proj["name"], f"${proj['payment']:.2f}")

        self.app.console.print(table)

        input("\nPress ENTER to return...")
        self.app.change_screen("index")
