from p2.src.Studium import ModulStatus
from p2.src.Pruefungsleistung import Pruefungsleistung
from p2.src.Studium import Pruefungsform


from dataclasses import dataclass


@dataclass
class Modul:
    kurs_id: str
    kursname: str
    ects: int
    pruefungsform: Pruefungsform
    status: ModulStatus = ModulStatus.OFFEN
    pruefungsleistung: Pruefungsleistung | None = None

    def add_pruefungsleistung(self, note: float) -> None:
        if self.pruefungsleistung is not None and self.pruefungsleistung.ist_bestanden:
            raise ValueError("Das Modul ist bereits bestanden.")

        if self.pruefungsleistung is None:
            neuer_versuch = 1
        else:
            neuer_versuch = self.pruefungsleistung.versuch + 1

        self.pruefungsleistung = Pruefungsleistung(
            note=note,
            versuch=neuer_versuch
        )

        if self.pruefungsleistung.ist_bestanden:
            self.status = ModulStatus.FERTIG
        else:
            self.status = ModulStatus.IN_ARBEIT

    def __repr__(self):
        return f"""
        Modul(
                kurs_id={self.kurs_id!r},
                kursname={self.kursname},
                ects={self.ects},
                pruefungsform={self.pruefungsform},
                status={self.status},
                pruefungsleistung={self.pruefungsleistung}
        )"""