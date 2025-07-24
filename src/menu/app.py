from __future__ import annotations
from rich.console import Console
from src.menu.pages.screen import Screen
from src.employee.queries import EmployeeStore
from src.employee.vacations import VacationService
from src.employee.payment import PaymentService
from src.logs.event_manager import EventManager
from src.logs.listener import Listener
from src.logs.events import Events
from src.logs.text_logger import TextLogger
from src.logs.employee_logger import EmployeeTransactionLogger

# import all the screens
import src.menu.pages.index
import src.menu.pages.filter_employees
import src.menu.pages.create_employee_form
import src.menu.pages.grant_vacations
import src.menu.pages.pay_employees
import src.menu.pages.employee_transactions
import src.menu.pages.freelance_projects

# Context class
class App:
    def __init__(self, employee_store: EmployeeStore, logging_system: Listener = TextLogger(), initial_view="index"):
        self.console = Console()
        self.running = True
        # register all the views inside the application
        self.screens = {}

        # Dependency Injection
        self.employee_store: EmployeeStore = employee_store
        self.vacation_service = VacationService()
        self.payment_service = PaymentService()

        # Store reference to the logging component
        self.event_manager = EventManager()
        self._setup_events(logging_system)

        for view in Screen.__subclasses__():
            v = view(self)
            print("this is the info:", v.view_name, v)
            self.screens[v.view_name] = v

        self.current_screen = self.screens[initial_view]

    def change_screen(self, screen_name: str):
        self.console.clear()
        self.current_screen = self.screens[screen_name]

    def run(self):
        while self.running:
            self.current_screen.render()
            user_input = input(">> ")
            self.current_screen.handle_input(user_input)


    def _setup_events(self, logger: Listener):
        """
        By default, this method uses the same logging system for all of the events.
        Of course, this could be easily modified for a more granular control over the events
        with different types of loggers or external providers.
        """
        self.event_manager.subscribe(Events.PAYMENT_EVENT, logger)
        self.event_manager.subscribe(Events.VACATION_EVENT, logger)
        self.event_manager.subscribe(Events.BONUS_PAYMENT_EVENT, logger)

        employee_logger = EmployeeTransactionLogger()
        self.event_manager.subscribe(Events.PAYMENT_EVENT, employee_logger)
        self.event_manager.subscribe(Events.VACATION_EVENT, employee_logger)
        self.event_manager.subscribe(Events.BONUS_PAYMENT_EVENT, employee_logger)