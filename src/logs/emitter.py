from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from src.logs.listener import Listener

class Emitter(ABC):

    @abstractmethod
    def attach(self, observer: Listener) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Listener) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass