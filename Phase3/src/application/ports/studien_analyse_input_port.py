from abc import ABC, abstractmethod
from datetime import date

from application.dtos.dashboard_daten import DashboardDaten


class StudienAnalyseInputPort(ABC):
    @abstractmethod
    def dashboard_daten_abrufen(self, stichtag: date | None = None) -> DashboardDaten:
        pass
