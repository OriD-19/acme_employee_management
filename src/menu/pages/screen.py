from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.menu.app import App

# State class
class Screen(ABC):
    """
    A screen represents a page inside the program.
    A screen could be composed of different components.
    Different types of screens are represented by specific classes,
    although this Screen interface can be used directly.
    """
    view_name: str

    def __init__(self, app: App):
        self.app = app

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_input(self, user_input: str):
        pass