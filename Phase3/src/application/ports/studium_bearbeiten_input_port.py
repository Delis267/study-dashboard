from abc import ABC, abstractmethod

from domain.pruefungsform import Pruefungsform

class StudiumBearbeitenInputPort(ABC):
    @abstractmethod
    def modul_hinzufuegen(
        self,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform,
        ist_anerkannt: bool = False # Default False, optional bei Modulanlage
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
            pruefungsform: Pruefungsform, 
            note: float | None) -> None:
        '''Der Kursname, die ECTS-Punkte, die Prüfungsform und die Note eines Moduls werden bearbeitet.
        Note ist der einzige optionale Parameter.'''
        pass
