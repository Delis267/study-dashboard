from abc import ABC, abstractmethod

from domain.studium import Studium

class StudiumRepositoryPort(ABC):
    @abstractmethod
    def laden(self) -> Studium:
        pass

    @abstractmethod
    def speichern(self, studium: Studium) -> None:
        pass
