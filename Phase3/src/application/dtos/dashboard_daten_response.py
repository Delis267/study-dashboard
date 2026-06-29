from dataclasses import dataclass
from datetime import date

from domain.modul_status import ModulStatus


@dataclass(frozen=True)
class PruefungsversuchDaten:
    note: float
    ist_bestanden: bool


@dataclass(frozen=True)
class ModulDaten:
    kurs_id: str
    kursname: str
    ects: int
    status: ModulStatus
    pruefungsform: str | None
    note: float | None
    versuche: tuple[PruefungsversuchDaten, ...]


@dataclass(frozen=True)
class DashboardDatenResponse:
    studiengang: str
    startdatum: date
    zieldatum: date
    gesamt_ects: int
    erreichte_ects: int
    offene_ects: int
    fortschritt_prozent: float
    ects_nach_status: dict[ModulStatus, int]
    notendurchschnitt: float | None
    ziel_notendurchschnitt: float
    ziel_notendurchschnitt_erreicht: bool | None
    velocity_ects_pro_monat: float
    ziel_velocity_ects_pro_monat: float
    prognostiziertes_ende: date | None
    module: list[ModulDaten]
