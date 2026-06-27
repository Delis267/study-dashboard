from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.studium import Studium

from application.dtos.studium_bearbeiten_requests import ModulHinzufuegenRequest
from application.ports.studium_bearbeiten_use_case import StudiumBearbeitenUseCase
from application.ports.studium_repository_port import StudiumRepositoryPort


class StudiumBearbeitenService(StudiumBearbeitenUseCase):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def modul_hinzufuegen(self, request: ModulHinzufuegenRequest) -> None:
        studium = self.repository.laden()

        if request.ist_anerkannt:
            modul = Modul(
                kurs_id=request.kurs_id,
                kursname=request.kursname,
                ects=request.ects,
                pruefungsleistung=None,
                status=ModulStatus.ANERKANNT,
            )
        else:
            modul = Modul(
                kurs_id=request.kurs_id,
                kursname=request.kursname,
                ects=request.ects,
                pruefungsleistung=Pruefungsleistung(request.pruefungsform),
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
        pruefungsform: Pruefungsform | None,
        note: float | None,
    ) -> None:
        studium = self.repository.laden()
        modul = self._modul_oder_fehler(studium, kurs_id)

        modul.basisdaten_aendern(kursname=kursname, ects=ects)

        if note is not None:
            modul.note_eintragen(note)

        if pruefungsform is not None:
            modul.pruefungsform_aendern(pruefungsform)

        self.repository.speichern(studium)

    def _modul_oder_fehler(self, studium: Studium, kurs_id: str) -> Modul:
        modul = studium.modul_finden(kurs_id)
        if modul is None:
            raise ValueError("Modul nicht gefunden.")
        return modul
