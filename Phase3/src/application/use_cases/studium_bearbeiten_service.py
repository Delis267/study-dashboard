from domain.modul import Modul
from domain.studium import Studium

from application.dtos.studium_bearbeiten_requests import ModulBearbeitenRequest, ModulHinzufuegenRequest
from application.ports.studium_bearbeiten_use_case import StudiumBearbeitenUseCase
from application.ports.studium_repository_port import StudiumRepositoryPort


class StudiumBearbeitenService(StudiumBearbeitenUseCase):
    def __init__(self, repository: StudiumRepositoryPort) -> None:
        self.repository = repository

    def modul_hinzufuegen(self, request: ModulHinzufuegenRequest) -> None:
        studium = self.repository.laden()
        studium.modul_hinzufuegen(request.to_modul())
        self.repository.speichern(studium)

    def modul_loeschen(self, kurs_id: str) -> None:
        studium = self.repository.laden()
        studium.modul_entfernen(kurs_id)
        self.repository.speichern(studium)

    def modul_bearbeiten(self, request: ModulBearbeitenRequest) -> None:
        studium = self.repository.laden()

        modul = self._modul_oder_fehler(studium, request.kurs_id)
        modul.basisdaten_aendern(kursname=request.kursname, ects=request.ects)

        if request.note is not None:
            modul.note_eintragen(request.note)

        if request.pruefungsform is not None:
            modul.pruefungsform_aendern(request.pruefungsform)

        self.repository.speichern(studium)

    def _modul_oder_fehler(self, studium: Studium, kurs_id: str) -> Modul:
        modul = studium.modul_finden(kurs_id)
        if modul is None:
            raise ValueError("Modul nicht gefunden.")
        return modul
