from dataclasses import dataclass
from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.pruefungsform import Pruefungsform


@dataclass(frozen=True)
class ModulHinzufuegenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    ist_anerkannt: bool = False
    
    def to_modul(self):
        if self.ist_anerkannt:
            modul = Modul(
                kurs_id=self.kurs_id,
                kursname=self.kursname,
                ects=self.ects,
                pruefungsleistung=None,
                status=ModulStatus.ANERKANNT,
            )
        else:
            modul = Modul(
                kurs_id=self.kurs_id,
                kursname=self.kursname,
                ects=self.ects,
                pruefungsleistung=Pruefungsleistung(self.pruefungsform),
            )
        return modul
    
@dataclass(frozen=True)
class ModulBearbeitenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    note: float | None