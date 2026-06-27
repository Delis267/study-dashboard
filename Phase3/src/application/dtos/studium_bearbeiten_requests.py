from dataclasses import dataclass

from domain.pruefungsform import Pruefungsform


@dataclass(frozen=True)
class ModulHinzufuegenRequest:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform | None
    ist_anerkannt: bool = False
