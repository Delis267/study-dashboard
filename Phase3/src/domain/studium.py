from dataclasses import dataclass, field
from datetime import date, timedelta

from .modul import Modul
from .modul_status import ModulStatus


@dataclass
class Studium:
    studiengang: str
    startdatum: date
    zieldatum: date
    gesamt_ects: int
    ziel_notendurchschnitt: float
    module: list[Modul] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.studiengang.strip():
            raise ValueError("Der Studiengang darf nicht leer sein.")
        if self.startdatum >= self.zieldatum:
            raise ValueError("Das Startdatum muss vor dem Zieldatum liegen.")
        if self.gesamt_ects <= 0:
            raise ValueError("Gesamt-ECTS muessen groesser als 0 sein.")
        if not 1.0 <= self.ziel_notendurchschnitt <= 4.0:
            raise ValueError("Der Zielnotendurchschnitt muss zwischen 1.0 und 4.0 liegen.")

    def modul_hinzufuegen(self, modul: Modul) -> None:
        if self.modul_finden(modul.kurs_id) is not None:
            raise ValueError("Es duerfen keine zwei Module mit derselben Kurs-ID existieren.")
        self.module.append(modul)

    def modul_finden(self, kurs_id: str) -> Modul | None:
        for modul in self.module:
            if modul.kurs_id == kurs_id:
                return modul
        return None

    def modul_entfernen(self, kurs_id: str) -> None:
        modul = self.modul_finden(kurs_id)
        if modul is None:
            raise ValueError("Modul nicht gefunden.")
        self.module.remove(modul)

    def ects_fuer_status(self, *status_filter: ModulStatus) -> int:
        ''' Gibt die Summe der ECTS-Punkte für die angegebenen Modulstatus zurück.'''
        if not status_filter:
            raise ValueError("Es muss mindestens ein Modulstatus angegeben werden.")
        return sum(modul.ects for modul in self.module if modul.status in status_filter)

    @property
    def erreichte_ects(self) -> int:
        return self.ects_fuer_status(ModulStatus.FERTIG, ModulStatus.ANERKANNT)

    @property
    def eigenleistung_ects(self) -> int:
        return self.ects_fuer_status(ModulStatus.FERTIG)

    @property
    def offene_ects(self) -> int:
        return max(self.gesamt_ects - self.erreichte_ects, 0)

    @property
    def fortschritt_prozent(self) -> float:
        return round(self.erreichte_ects / self.gesamt_ects * 100, 2)

    @property
    def gewichteter_notendurchschnitt(self) -> float | None:
        benotete_module = [
            modul
            for modul in self.module
            if modul.status == ModulStatus.FERTIG and modul.aktuelle_note is not None
        ]
        gewichtete_ects = sum(modul.ects for modul in benotete_module)
        if gewichtete_ects == 0:
            return None

        gewichtete_summe = sum(modul.aktuelle_note * modul.ects for modul in benotete_module)
        return round(gewichtete_summe / gewichtete_ects, 2)

    @property
    def ziel_notendurchschnitt_erreicht(self) -> bool | None:
        notendurchschnitt = self.gewichteter_notendurchschnitt
        if notendurchschnitt is None:
            return None
        return notendurchschnitt <= self.ziel_notendurchschnitt
    
    @property
    def ziel_velocity(self) -> float:
        monate = self._monate_seit_start(self.zieldatum)
        return round(self.gesamt_ects / monate, 2)

    def velocity(self, stichtag: date) -> float:
        monate = self._monate_seit_start(stichtag)
        if monate == 0:
            return 0.0
        return round(self.eigenleistung_ects / monate, 2)

    def prognostiziertes_ende(self, stichtag: date) -> date | None:
        velocity = self.velocity(stichtag)
        if velocity == 0:
            return None

        monate_bis_abschluss = self.offene_ects / velocity
        tage_bis_abschluss = round(monate_bis_abschluss * 30.4375)
        return stichtag + timedelta(days=tage_bis_abschluss)

    def _monate_seit_start(self, stichtag: date) -> float:
        if stichtag < self.startdatum:
            raise ValueError("Der Stichtag darf nicht vor dem Studienstart liegen.")

        tage = (stichtag - self.startdatum).days
        return round(tage / 30.4375, 2)
