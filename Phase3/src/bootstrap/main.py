from datetime import date
from pathlib import Path

from application.use_cases.studien_analyse_service import StudienAnalyseService
from application.use_cases.studium_bearbeiten_service import StudiumBearbeitenService
from infrastructure.ui.dashboard_tkinter_app import DashboardTkinterApp
from infrastructure.persistence.json_studium_repository import JsonStudiumRepository


class Application:

    def starten(self, filename: str) -> None:
        datenpfad = Path(__file__).resolve().parents[2] / filename

        print("Starte Anwendung mit Datenpfad für das Json-Repository:", datenpfad)

        repository = JsonStudiumRepository(datenpfad)
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service = StudienAnalyseService(repository)
        
        app = DashboardTkinterApp(
            analyse_port=analyse_service,
            bearbeiten_port=bearbeiten_service,
        )

        app.starten()


if __name__ == "__main__":
    Application()\
        .starten("src/data/studium.json")
