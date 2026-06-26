from datetime import date
from pathlib import Path

from application.use_cases.studien_analyse_service import StudienAnalyseService
from application.use_cases.studium_bearbeiten_service import StudiumBearbeitenService
from infrastructure.ui.dashboard_tkinter_app import DashboardTkinterApp
from infrastructure.persistence.json_studium_repository import JsonStudiumRepository


class Application:
    def __init__(self) -> None:
        datenpfad = Path(__file__).resolve().parents[2] / "data" / "studium.json"
        repository = JsonStudiumRepository(datenpfad)
        self.bearbeiten_service = StudiumBearbeitenService(repository)
        self.analyse_service = StudienAnalyseService(repository)

    def demo_starten(self) -> None:
        dashboard_daten = self.analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1),
        )

        print("Studiengang:", dashboard_daten.studiengang)
        print("Erreichte ECTS:", dashboard_daten.erreichte_ects)
        print("Offene ECTS:", dashboard_daten.offene_ects)
        print("Notendurchschnitt:", dashboard_daten.notendurchschnitt)
        print("Velocity:", dashboard_daten.velocity_ects_pro_monat)
        print("Prognose:", dashboard_daten.prognostiziertes_ende)

    def starten(self) -> None:
        app = DashboardTkinterApp(
            analyse_port=self.analyse_service,
            bearbeiten_port=self.bearbeiten_service,
        )
        app.starten()


if __name__ == "__main__":
    Application().starten()
