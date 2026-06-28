from dataclasses import dataclass, field

from .pruefungsform import Pruefungsform
from .pruefungsversuch import Pruefungsversuch


MAX_VERSUCHE = 3


@dataclass
class Pruefungsleistung:
    pruefungsform: Pruefungsform
    _versuche: list[Pruefungsversuch] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if self.pruefungsform is None:
            raise ValueError("Eine Pruefungsleistung braucht eine Pruefungsform.")

    def versuch_eintragen(self, note: float) -> None:
        if self.ist_bestanden:
            raise ValueError("Weitere Versuche sind nicht erlaubt: Pruefung bereits bestanden.")
        if len(self._versuche) >= MAX_VERSUCHE:
            raise ValueError("Maximale Anzahl Versuche erreicht.")

        self._versuche.append(Pruefungsversuch(note=note))

    def pruefungsform_aendern(self, pruefungsform: Pruefungsform) -> None:
        self.pruefungsform = pruefungsform
        
    @property
    def versuche(self) -> tuple[Pruefungsversuch, ...]:
        return tuple(self._versuche)

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
        return self.letzter_versuch is not None and self.letzter_versuch.ist_bestanden

    @property
    def ist_endgueltig_nicht_bestanden(self) -> bool:
        return (
            self.letzter_versuch is not None
            and not self.letzter_versuch.ist_bestanden
            and len(self._versuche) >= MAX_VERSUCHE
        )
