from dataclasses import dataclass
from .modul_status import ModulStatus
from .pruefungsform import Pruefungsform
from .pruefungsleistung import Pruefungsleistung


@dataclass
class Modul:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsleistung: Pruefungsleistung | None

    @classmethod
    def regulaer(
        cls,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform,
    ) -> "Modul":
        return cls(
            kurs_id=kurs_id,
            kursname=kursname,
            ects=ects,
            pruefungsleistung=Pruefungsleistung(pruefungsform),
        )

    @classmethod
    def anerkannt(
        cls,
        kurs_id: str,
        kursname: str,
        ects: int,
    ) -> "Modul":
        return cls(
            kurs_id=kurs_id,
            kursname=kursname,
            ects=ects,
            pruefungsleistung=None,
        )

    @property
    def ist_anerkannt(self) -> bool:
        return self.pruefungsleistung is None

    @property
    def status(self) -> ModulStatus:
        if self.ist_anerkannt:
            return ModulStatus.ANERKANNT
        if not self.pruefungsleistung.versuche:
            return ModulStatus.OFFEN
        if self.pruefungsleistung.ist_bestanden:
            return ModulStatus.FERTIG
        return ModulStatus.IN_ARBEIT

    def __post_init__(self) -> None:
        if not self.kurs_id.strip():
            raise ValueError("Die Kurs-ID darf nicht leer sein.")
        if not self.kursname.strip():
            raise ValueError("Der Kursname darf nicht leer sein.")
        if self.ects <= 0:
            raise ValueError("ECTS muessen groesser als 0 sein.")

    def note_eintragen(self, note: float) -> None:
        if self.ist_anerkannt:
            raise ValueError("Fuer anerkannte Module kann keine Note eingetragen werden.")

        self.pruefungsleistung.versuch_eintragen(note)

    def pruefungsform_aendern(self, pruefungsform: Pruefungsform) -> None:
        if self.ist_anerkannt:
            raise ValueError("Fuer anerkannte Module kann die Pruefungsform nicht geaendert werden.")

        self.pruefungsleistung.pruefungsform_aendern(pruefungsform)

    def basisdaten_aendern(
        self,
        kursname: str | None = None,
        ects: int | None = None,
    ) -> None:
        if kursname is not None:
            if not kursname.strip():
                raise ValueError("Der Kursname darf nicht leer sein.")
            self.kursname = kursname

        if ects is not None:
            if ects <= 0:
                raise ValueError("ECTS muessen groesser als 0 sein.")
            self.ects = ects

    def anerkennen(self) -> None:
        if self.pruefungsleistung is not None and self.pruefungsleistung.versuche:
            raise ValueError("Module mit Pruefungsversuchen koennen nicht anerkannt werden.")

        self.pruefungsleistung = None
            
    @property
    def aktuelle_note(self) -> float | None:
        if self.pruefungsleistung is None or self.pruefungsleistung.letzter_versuch is None:
            return None
        if not self.pruefungsleistung.ist_bestanden:
            return None
        return self.pruefungsleistung.letzter_versuch.note

    def __str__(self) -> str:
        return (
            f"Modul(id={self.kurs_id}, name={self.kursname}, "
            f"ects={self.ects}, status={self.status}, "
            f"pruefungsleistung={self.pruefungsleistung})"
        )
