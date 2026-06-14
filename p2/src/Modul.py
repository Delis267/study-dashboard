from dataclasses import dataclass, field
from Pruefungsleistung import Pruefungsleistung
from ModulStatus import ModulStatus
from Pruefungsform import Pruefungsform

@dataclass
class Modul:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform
    status: ModulStatus = ModulStatus.OFFEN
    pruefungsleistung: Pruefungsleistung = field(default_factory=Pruefungsleistung)

    def note_eintragen(self, note: float) -> None:
        # Delegation an Pruefungsleistung, keine Noten-/Versuchslogik im Modul
        self.pruefungsleistung.versuch_eintragen(note)
        self._status_aktualisieren()

    def _status_aktualisieren(self) -> None:
        if self.pruefungsleistung.ist_bestanden:
            self.status = ModulStatus.FERTIG
        elif not self.pruefungsleistung.versuche:
            self.status = ModulStatus.OFFEN
        else:
            self.status = ModulStatus.IN_ARBEIT

    def __repr__(self) -> str:
        return          f"Modul(kurs_id={self.kurs_id!r}, kursname={self.kursname!r}, ects={self.ects}"