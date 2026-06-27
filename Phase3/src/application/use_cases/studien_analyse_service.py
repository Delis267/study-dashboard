from datetime import date

from application.dtos.dashboard_daten import (
    DashboardDaten,
    ModulDaten,
    PruefungsversuchDaten,
)
from application.ports.studien_analyse_input_port import StudienAnalyseInputPort
from application.ports.studium_repository_port import StudiumRepositoryPort
from domain.modul import Modul


class StudienAnalyseService(StudienAnalyseInputPort):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def dashboard_daten_abrufen(
        self,
        stichtag: date | None = None,
    ) -> DashboardDaten:
        if stichtag is None:
            stichtag = date.today()

        studium = self.repository.laden()
        return DashboardDaten(
            studiengang=studium.studiengang,
            startdatum=studium.startdatum,
            zieldatum=studium.zieldatum,
            gesamt_ects=studium.gesamt_ects,
            erreichte_ects=studium.erreichte_ects,
            offene_ects=studium.offene_ects,
            fortschritt_prozent=studium.fortschritt_prozent,
            ects_nach_status=studium.ects_nach_status,
            notendurchschnitt=studium.gewichteter_notendurchschnitt,
            ziel_notendurchschnitt=studium.ziel_notendurchschnitt,
            ziel_notendurchschnitt_erreicht=studium.ziel_notendurchschnitt_erreicht,
            velocity_ects_pro_monat=studium.velocity(stichtag),
            ziel_velocity_ects_pro_monat=studium.ziel_velocity,
            prognostiziertes_ende=studium.prognostiziertes_ende(stichtag),
            module=[self._modul_daten_erstellen(modul) for modul in studium.module],
        )

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
