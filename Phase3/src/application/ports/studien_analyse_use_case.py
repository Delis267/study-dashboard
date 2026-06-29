from abc import ABC, abstractmethod
from datetime import date

from application.dtos.dashboard_daten_response import DashboardDatenResponse

class StudienAnalyseUseCase(ABC):
    @abstractmethod
    def dashboard_daten_abrufen(self, stichtag: date | None = None) -> DashboardDatenResponse:
        pass
