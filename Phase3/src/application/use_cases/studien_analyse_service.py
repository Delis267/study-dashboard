from datetime import date

from application.dtos.dashboard_daten import DashboardDaten, ModulDaten
from application.ports.studien_analyse_input_port import StudienAnalyseInputPort
from application.ports.studium_repository_port import StudiumRepositoryPort


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
            prognostiziertes_ende=studium.prognostiziertes_ende(stichtag),
            module=[
                ModulDaten(
                    kurs_id=modul.kurs_id,
                    kursname=modul.kursname,
                    ects=modul.ects,
                    status=modul.status,
                    pruefungsform=(
                        None
                        if modul.pruefungsleistung is None
                        else modul.pruefungsleistung.pruefungsform.value
                    ),
                    note=modul.aktuelle_note,
                )
                for modul in studium.module
            ],
        )
