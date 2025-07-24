from abc import ABC, abstractmethod

class Listener(ABC):

    @abstractmethod
    def update(self, payload) -> None:
        pass