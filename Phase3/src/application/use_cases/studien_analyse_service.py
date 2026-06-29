from datetime import date

from application.dtos.dashboard_daten_response import (
    DashboardDatenResponse,
    ModulDaten,
    PruefungsversuchDaten,
)
from application.ports.studien_analyse_use_case import StudienAnalyseUseCase
from application.ports.studium_repository_port import StudiumRepositoryPort
from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.studium import Studium


class StudienAnalyseService(StudienAnalyseUseCase):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def dashboard_daten_abrufen(self, stichtag: date | None = None,) -> DashboardDatenResponse:
        if stichtag is None:
            stichtag = date.today()

        studium = self.repository.laden()

        erreichte_ects = self._erreichte_ects(studium)
        offene_ects = self._offene_ects(studium, erreichte_ects)

        return DashboardDatenResponse(
            studiengang=studium.studiengang,
            startdatum=studium.startdatum,
            zieldatum=studium.zieldatum,
            gesamt_ects=studium.gesamt_ects,
            erreichte_ects=erreichte_ects,
            offene_ects=offene_ects,
            fortschritt_prozent=self._fortschritt_prozent(studium, erreichte_ects),
            ects_nach_status=self._ects_nach_status_erstellen(studium),
            notendurchschnitt=studium.gewichteter_notendurchschnitt,
            ziel_notendurchschnitt=studium.ziel_notendurchschnitt,
            ziel_notendurchschnitt_erreicht=studium.ziel_notendurchschnitt_erreicht,
            velocity_ects_pro_monat=studium.velocity(stichtag),
            ziel_velocity_ects_pro_monat=studium.ziel_velocity,
            prognostiziertes_ende=studium.prognostiziertes_ende(stichtag),
            module=[self._modul_daten_erstellen(modul) for modul in studium.module],
        )

    def _erreichte_ects(self, studium: Studium) -> int:
        return studium.ects_fuer_status(ModulStatus.FERTIG, ModulStatus.ANERKANNT)

    def _offene_ects(self, studium: Studium, erreichte_ects: int) -> int:
        return max(studium.gesamt_ects - erreichte_ects, 0)

    def _fortschritt_prozent(self, studium: Studium, erreichte_ects: int) -> float:
        return round(erreichte_ects / studium.gesamt_ects * 100, 2)

    def _ects_nach_status_erstellen(self, studium: Studium) -> dict[ModulStatus, int]:
        return {
            status: studium.ects_fuer_status(status)
            for status in ModulStatus
        }

    def _modul_daten_erstellen(self, modul: Modul) -> ModulDaten:
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
