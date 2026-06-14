from dataclasses import dataclass, field
from typing import Optional
from Pruefungsversuch import Pruefungsversuch


@dataclass
class Pruefungsleistung:
    max_versuche: int = 3
    versuche: list[Pruefungsversuch] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.max_versuche < 1:
            raise ValueError("max_versuche muss >= 1 sein.")
        # Validierung bestehender Versuche (falls übergeben)
        nummern = [v.nummer for v in self.versuche]
        if len(nummern) != len(set(nummern)):
            raise ValueError("Versuchsnummern müssen eindeutig sein.")
        if nummern and (min(nummern) != 1 or sorted(nummern) != list(range(1, len(nummern) + 1))):
            raise ValueError("Versuche müssen fortlaufend ab 1 nummeriert sein.")
        if len(self.versuche) > self.max_versuche:
            raise ValueError("Es wurden mehr Versuche als erlaubt übergeben.")

    def versuch_eintragen(self, note: float) -> Pruefungsversuch:
        if self.ist_bestanden:
            raise ValueError("Weitere Versuche sind nicht erlaubt: Prüfung bereits bestanden.")
        if self.ist_endgueltig_nicht_bestanden:
            raise ValueError("Weitere Versuche sind nicht erlaubt: Maximale Anzahl Versuche erreicht.")
        naechste_nummer = len(self.versuche) + 1
        if naechste_nummer > self.max_versuche:
            raise ValueError("Maximale Anzahl Versuche erreicht.")
        neuer_versuch = Pruefungsversuch(nummer=naechste_nummer, note=note)
        self.versuche.append(neuer_versuch)
        return neuer_versuch

    @property
    def letzter_versuch(self) -> Optional[Pruefungsversuch]:
        if not self.versuche:
            return None
        return self.versuche[-1]

    @property
    def naechster_versuch(self) -> Optional[int]:
        if self.ist_bestanden:
            return None
        if len(self.versuche) >= self.max_versuche:
            return None
        return len(self.versuche) + 1

    @property
    def ist_bestanden(self) -> bool:
        return any(v.note <= 4.0 for v in self.versuche)

    @property
    def ist_endgueltig_nicht_bestanden(self) -> bool:
        return (len(self.versuche) >= self.max_versuche) and (not self.ist_bestanden)

    def __repr__(self) -> str:
        return f"Pruefungsleistung(max_versuche={self.max_versuche}, versuche={self.versuche})"