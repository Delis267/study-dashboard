from abc import ABC, abstractmethod

from application.dtos.studium_bearbeiten_requests import ModulBearbeitenRequest, ModulHinzufuegenRequest
from domain.pruefungsform import Pruefungsform

class StudiumBearbeitenUseCase(ABC):
    @abstractmethod
    def modul_hinzufuegen(self, request: ModulHinzufuegenRequest) -> None:
        pass

    @abstractmethod
    def modul_loeschen(self, kurs_id: str) -> None:
        pass

    @abstractmethod
    def modul_bearbeiten(self, request: ModulBearbeitenRequest) -> None:
        pass

