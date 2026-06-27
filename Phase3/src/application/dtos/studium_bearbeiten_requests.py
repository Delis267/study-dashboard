from dataclasses import dataclass
from domain.modul import Modul
from domain.pruefungsform import Pruefungsform


@dataclass(frozen=True)
class ModulHinzufuegenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    ist_anerkannt: bool = False
    
    def to_modul(self) -> Modul:
        if self.ist_anerkannt:
            return Modul.anerkannt(
                self.kurs_id,
                self.kursname,
                self.ects,
            )

        if self.pruefungsform is None:
            raise ValueError("Nicht anerkannte Module brauchen eine Pruefungsform.")

        return Modul.regulaer(
            self.kurs_id,
            self.kursname,
            self.ects,
            self.pruefungsform,
        )
    
@dataclass(frozen=True)
class ModulBearbeitenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    note: float | None
