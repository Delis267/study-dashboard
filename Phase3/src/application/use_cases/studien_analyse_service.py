from datetime import date

from application.dtos.dashboard_daten_response import DashboardDatenResponse
from application.ports.studien_analyse_use_case import StudienAnalyseUseCase
from application.ports.studium_repository_port import StudiumRepositoryPort


class StudienAnalyseService(StudienAnalyseUseCase):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def dashboard_daten_abrufen(self, stichtag: date | None = None,) -> DashboardDatenResponse:
        if stichtag is None:
            stichtag = date.today()

        studium = self.repository.laden()
        
        return DashboardDatenResponse.from_studium(studium, stichtag)
