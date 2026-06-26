from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.studium import Studium

from application.ports.studium_bearbeiten_input_port import StudiumBearbeitenInputPort
from application.ports.studium_repository_port import StudiumRepositoryPort


class StudiumBearbeitenService(StudiumBearbeitenInputPort):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def modul_hinzufuegen(
        self,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform | None,
        ist_anerkannt: bool = False,
    ) -> None:
        studium = self.repository.laden()
        if ist_anerkannt or pruefungsform is None:
            modul = Modul(
                kurs_id=kurs_id,
                kursname=kursname,
                ects=ects,
                pruefungsleistung=None,
                status=ModulStatus.ANERKANNT,
            )
        else:
            modul = Modul(
                kurs_id=kurs_id,
                kursname=kursname,
                ects=ects,
                pruefungsleistung=Pruefungsleistung(pruefungsform),
            )
        studium.modul_hinzufuegen(modul)
        self.repository.speichern(studium)

    def modul_loeschen(self, kurs_id: str) -> None:
        studium = self.repository.laden()
        studium.modul_entfernen(kurs_id)
        self.repository.speichern(studium)

    def modul_bearbeiten(
        self,
        kurs_id: str,
        kursname: str,
        ects: int,
        pruefungsform: Pruefungsform,
        note: float | None,
    ) -> None:
        studium = self.repository.laden()
        modul = self._modul_oder_fehler(studium, kurs_id)

        if modul.status == ModulStatus.ANERKANNT:
            if note is not None:
                raise ValueError("Fuer anerkannte Module kann keine Note eingetragen werden.")
            modul.daten_aendern(kursname=kursname, ects=ects)
        else:
            modul.daten_aendern(
                kursname=kursname,
                ects=ects,
                pruefungsleistung=Pruefungsleistung(pruefungsform),
            )
            if note is not None:
                modul.note_eintragen(note)

        self.repository.speichern(studium)

    def _modul_oder_fehler(self, studium: Studium, kurs_id: str) -> Modul:
        modul = studium.modul_finden(kurs_id)
        if modul is None:
            raise ValueError("Modul nicht gefunden.")
        return modul
