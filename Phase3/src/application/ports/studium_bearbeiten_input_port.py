from abc import ABC, abstractmethod

from domain.pruefungsform import Pruefungsform


class StudiumBearbeitenInputPort(ABC):
    @abstractmethod
    def modul_hinzufuegen(
        self,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform | None,
        ist_anerkannt: bool = False,
    ) -> None:
        pass

    @abstractmethod
    def modul_loeschen(self, kurs_id: str) -> None:
        pass

    @abstractmethod
    def modul_bearbeiten(
        self,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform | None,
        note: float | None,
    ) -> None:
        pass
