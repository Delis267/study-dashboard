from dataclasses import dataclass
from modul_status import ModulStatus
from pruefungsleistung import Pruefungsleistung

@dataclass
class Modul:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsleistung: Pruefungsleistung
    status: ModulStatus = ModulStatus.OFFEN

    def note_eintragen(self, note: float) -> None:
        self.pruefungsleistung.versuch_eintragen(note)
        self._status_aktualisieren()

    def _status_aktualisieren(self) -> None:
        if self.status == ModulStatus.ANERKANNT:
            return
        if not self.pruefungsleistung._versuche:
            self.status = ModulStatus.OFFEN
        elif self.pruefungsleistung.ist_bestanden:
            self.status = ModulStatus.FERTIG
        else:
            self.status = ModulStatus.IN_ARBEIT

    def __str__(self) -> str:
        return (
            f"Modul(id={self.kurs_id}, name={self.kursname}, "
            f"status={self.status}, {self.pruefungsleistung})"
        )
