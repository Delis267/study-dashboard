from enum import Enum
from p2.src.Modul import Modul
from p2.src.Modul import Modul
from dataclasses import dataclass, field
from datetime import date

class Pruefungsform(Enum):
    KLAUSUR = "Klausur"
    HAUSARBEIT = "Hausarbeit"
    PORTFOLIO = "Portfolio"
    PROJEKT = "Projekt"
    SEMINAR = "Seminar"
    PRAESENTATION = "Praesentation"
    BACHELORARBEIT = "Bachelorarbeit"

    def __str__(self):
        return self.name
    
class ModulStatus(Enum):
    OFFEN = "Offen"
    IN_ARBEIT = "In Arbeit"
    FERTIG = "Fertig"
    ANERKANNT = "Anerkannt"

    def __str__(self):
        return self.name


@dataclass
class Studium:
    studiengang: str
    startdatum: date
    zieldatum: date
    gesamt_ects: int
    ziel_notendurchschnitt: float
    module: list[Modul] = field(default_factory=list)

    def modul_hinzufuegen(self, modul: Modul) -> None:
        for module in self.module:
            if module.kurs_id == modul.kurs_id:
                raise ValueError("Es dürfen keine zwei Module mit der selben Kurs_ID existieren.")

        self.module.append(modul)

    @property
    def erreichte_ects(self) -> int:
        return sum(
            modul.ects
            for modul in self.module
            if modul.status in (ModulStatus.FERTIG, ModulStatus.ANERKANNT)
        )

    @property
    def fortschritt_prozent(self) -> float:
        if self.gesamt_ects == 0:
            return 0.0
        return self.erreichte_ects / self.gesamt_ects * 100

    def printModule(self):
        for module in self.module:
            print(module)

