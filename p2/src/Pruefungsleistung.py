from dataclasses import dataclass, field
from pruefungsform import Pruefungsform
from pruefungsversuch import Pruefungsversuch

@dataclass
class Pruefungsleistung:
    pruefungsform: Pruefungsform
    _MAX_VERSUCHE = 3
    _versuche: list[Pruefungsversuch] = field(default_factory=list, init=False)

    def versuch_eintragen(self, note: float) -> None:
        if self.ist_bestanden:
            raise ValueError("Weitere Versuche sind nicht erlaubt: Pruefung bereits bestanden.")
        if len(self._versuche) >= self._MAX_VERSUCHE:
            raise ValueError("Maximale Anzahl Versuche erreicht.")

        self._versuche.append(Pruefungsversuch(note=note))

    @property
    def versuche_anzahl(self) -> int:
        return len(self._versuche)

    @property
    def letzter_versuch(self) -> Pruefungsversuch | None:
        if not self._versuche:
            return None
        return self._versuche[-1]

    @property
    def ist_bestanden(self) -> bool:
        if self.letzter_versuch is None:
            return False
        return self.letzter_versuch.ist_bestanden

    def __str__(self) -> str:
        return (
            f"Pruefungsleistung("
            f"pruefungsform={self.pruefungsform}, "
            f"versuche={self.versuche_anzahl}, "
            f"letzter_versuch={self.letzter_versuch})"
        )
