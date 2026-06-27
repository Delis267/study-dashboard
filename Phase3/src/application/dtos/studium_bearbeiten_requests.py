from dataclasses import dataclass
from domain.pruefungsform import Pruefungsform


@dataclass(frozen=True)
class ModulHinzufuegenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    note: float | None = None
    ist_anerkannt: bool = False


@dataclass(frozen=True)
class ModulBearbeitenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    note: float | None
