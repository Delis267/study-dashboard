from dataclasses import dataclass, field
from datetime import date
from modul import Modul
from modul_status import ModulStatus

@dataclass
class Studium:
    studiengang: str
    startdatum: date
    zieldatum: date
    gesamt_ects: int
    ziel_notendurchschnitt: float
    module: list[Modul] = field(default_factory=list)

    def modul_hinzufuegen(self, modul: Modul) -> None:
        for vorhandenes_modul in self.module:
            if vorhandenes_modul.kurs_id == modul.kurs_id:
                raise ValueError("Es duerfen keine zwei Module mit derselben Kurs-ID existieren.")
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
        return round(self.erreichte_ects / self.gesamt_ects * 100, 2)

    def status_ausgeben(self) -> None:
        print("Studiengang:", self.studiengang)
        print("Zeitraum:", self.startdatum, "bis", self.zieldatum)
        print("Erreichte ECTS:", self.erreichte_ects, "von", self.gesamt_ects)
        print("Fortschritt in Prozent:", self.fortschritt_prozent)
        print("Module:")
        for modul in self.module:
            print("-", modul)
        print()    
