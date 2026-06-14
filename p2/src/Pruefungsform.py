from enum import Enum

class Pruefungsform(Enum):
    KLAUSUR = "Klausur"
    HAUSARBEIT = "Hausarbeit"
    PORTFOLIO = "Portfolio"
    PROJEKT = "Projekt"
    SEMINAR = "Seminar"
    PRAESENTATION = "Praesentation"
    BACHELORARBEIT = "Bachelorarbeit"

    def __str__(self) -> str:
        return self.name