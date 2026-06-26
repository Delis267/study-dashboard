from dataclasses import dataclass

from .modul_status import ModulStatus
from .pruefungsleistung import Pruefungsleistung


@dataclass
class Modul:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsleistung: Pruefungsleistung | None
    status: ModulStatus = ModulStatus.OFFEN

    def __post_init__(self) -> None:
        if not self.kurs_id.strip():
            raise ValueError("Die Kurs-ID darf nicht leer sein.")
        if not self.kursname.strip():
            raise ValueError("Der Kursname darf nicht leer sein.")
        if self.ects <= 0:
            raise ValueError("ECTS muessen groesser als 0 sein.")
        if self.status == ModulStatus.ANERKANNT and self.pruefungsleistung is not None:
            raise ValueError("Anerkannte Module haben keine Pruefungsleistung.")
        if self.status != ModulStatus.ANERKANNT and self.pruefungsleistung is None:
            raise ValueError("Nicht anerkannte Module brauchen eine Pruefungsleistung.")

    def note_eintragen(self, note: float) -> None:
        if self.pruefungsleistung is None:
            raise ValueError("Fuer anerkannte Module kann keine Note eingetragen werden.")

        self.pruefungsleistung.versuch_eintragen(note)
        self._status_aktualisieren()

    def anerkennen(self) -> None:
        if self.pruefungsleistung is not None and self.pruefungsleistung.versuche:
            raise ValueError("Module mit Pruefungsversuchen koennen nicht anerkannt werden.")

        self.pruefungsleistung = None
        self.status = ModulStatus.ANERKANNT

    def daten_aendern(
        self,
        kursname: str | None = None,
        ects: int | None = None,
        pruefungsleistung: Pruefungsleistung | None = None,
    ) -> None:
        if kursname is not None:
            if not kursname.strip():
                raise ValueError("Der Kursname darf nicht leer sein.")
            self.kursname = kursname

        if ects is not None:
            if ects <= 0:
                raise ValueError("ECTS muessen groesser als 0 sein.")
            self.ects = ects

        if pruefungsleistung is not None:
            if self.status == ModulStatus.ANERKANNT:
                raise ValueError("Anerkannte Module haben keine Pruefungsleistung.")
            self.pruefungsleistung = pruefungsleistung
            self._status_aktualisieren()

    @property
    def aktuelle_note(self) -> float | None:
        if self.pruefungsleistung is None or self.pruefungsleistung.letzter_versuch is None:
            return None
        if not self.pruefungsleistung.ist_bestanden:
            return None
        return self.pruefungsleistung.letzter_versuch.note

    def _status_aktualisieren(self) -> None:
        if self.status == ModulStatus.ANERKANNT:
            return
        if self.pruefungsleistung is None:
            raise ValueError("Nicht anerkannte Module brauchen eine Pruefungsleistung.")
        if not self.pruefungsleistung.versuche:
            self.status = ModulStatus.OFFEN
        elif self.pruefungsleistung.ist_bestanden:
            self.status = ModulStatus.FERTIG
        else:
            self.status = ModulStatus.IN_ARBEIT

    def __str__(self) -> str:
        return (
            f"Modul(id={self.kurs_id}, name={self.kursname}, "
            f"ects={self.ects}, status={self.status}, "
            f"pruefungsleistung={self.pruefungsleistung})"
        )

