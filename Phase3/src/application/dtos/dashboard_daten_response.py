from dataclasses import dataclass
from datetime import date

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.studium import Studium


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

    @classmethod
    def from_studium(cls, studium: Studium, stichtag: date) -> "DashboardDatenResponse":
        return cls(
            studiengang=studium.studiengang,
            startdatum=studium.startdatum,
            zieldatum=studium.zieldatum,
            gesamt_ects=studium.gesamt_ects,
            erreichte_ects=studium.erreichte_ects,
            offene_ects=studium.offene_ects,
            fortschritt_prozent=studium.fortschritt_prozent,
            ects_nach_status=cls._ects_nach_status_erstellen(studium),
            notendurchschnitt=studium.gewichteter_notendurchschnitt,
            ziel_notendurchschnitt=studium.ziel_notendurchschnitt,
            ziel_notendurchschnitt_erreicht=studium.ziel_notendurchschnitt_erreicht,
            velocity_ects_pro_monat=studium.velocity(stichtag),
            ziel_velocity_ects_pro_monat=studium.ziel_velocity,
            prognostiziertes_ende=studium.prognostiziertes_ende(stichtag),
            module=[cls._modul_daten_erstellen(modul) for modul in studium.module],
        )

    @staticmethod
    def _ects_nach_status_erstellen(studium: Studium) -> dict[ModulStatus, int]:
        return {
            status: studium.ects_fuer_status(status)
            for status in ModulStatus
        }

    @staticmethod
    def _modul_daten_erstellen(modul: Modul) -> ModulDaten:
        pruefungsleistung = modul.pruefungsleistung
        pruefungsform = None
        versuche = ()

        if pruefungsleistung is not None:
            pruefungsform = pruefungsleistung.pruefungsform.value
            versuche = tuple(
                PruefungsversuchDaten(
                    note=versuch.note,
                    ist_bestanden=versuch.ist_bestanden,
                )
                for versuch in pruefungsleistung.versuche
            )

        return ModulDaten(
            kurs_id=modul.kurs_id,
            kursname=modul.kursname,
            ects=modul.ects,
            status=modul.status,
            pruefungsform=pruefungsform,
            note=modul.aktuelle_note,
            versuche=versuche,
        )
