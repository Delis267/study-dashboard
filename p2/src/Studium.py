from dataclasses import dataclass, field
from datetime import date
from Modul import Modul
from ModulStatus import ModulStatus

# Hinweis: Kein Import von Modul hier, um zirkuläre Importe zu vermeide

@dataclass
class Studium:
    studiengang: str
    startdatum: date
    zieldatum: date
    gesamt_ects: int
    ziel_notendurchschnitt: float
    module: list[Modul] = field(default_factory=list)

    def modul_hinzufuegen(self, modul: Modul) -> None:
        for m in self.module:
            if m.kurs_id == modul.kurs_id:
                raise ValueError("Es dürfen keine zwei Module mit derselben Kurs-ID existieren.")
        self.module.append(modul)

    @property
    def erreichte_ects(self) -> int:
        return sum(
            m.ects
            for m in self.module
            if m.status in (ModulStatus.FERTIG, ModulStatus.ANERKANNT)
        )

    @property
    def fortschritt_prozent(self) -> float:
        if self.gesamt_ects == 0:
            return 0.0
        return self.erreichte_ects / self.gesamt_ects * 100

    def print_module(self) -> None:
        for m in self.module:
            print(m)

