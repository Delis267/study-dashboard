import unittest
from datetime import date

from application.dtos.studium_bearbeiten_requests import (
    ModulBearbeitenRequest,
    ModulHinzufuegenRequest,
)
from application.ports.studien_analyse_use_case import StudienAnalyseUseCase
from application.ports.studium_bearbeiten_use_case import StudiumBearbeitenUseCase
from application.use_cases.studien_analyse_service import StudienAnalyseService
from application.use_cases.studium_bearbeiten_service import StudiumBearbeitenService
from domain.pruefungsform import Pruefungsform
from domain.studium import Studium


class InMemoryStudiumRepository:
    def __init__(self, studium: Studium) -> None:
        self.studium = studium
        self.wurde_gespeichert = False

    def laden(self) -> Studium:
        return self.studium

    def speichern(self, studium: Studium) -> None:
        self.studium = studium
        self.wurde_gespeichert = True


class InputPortsTest(unittest.TestCase):
    def test_bearbeiten_service_implementiert_frontend_port(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        service: StudiumBearbeitenUseCase = StudiumBearbeitenService(repository)

        service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )
        service.modul_bearbeiten(
            ModulBearbeitenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )

        modul = repository.studium.modul_finden("OOP")
        self.assertIsNotNone(modul)
        self.assertEqual(2.3, modul.aktuelle_note)
        self.assertTrue(repository.wurde_gespeichert)

    def test_modul_kann_ueber_frontend_port_bearbeitet_werden(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        service: StudiumBearbeitenUseCase = StudiumBearbeitenService(repository)

        service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )

        service.modul_bearbeiten(
            ModulBearbeitenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung und Design",
                ects=10,
                pruefungsform=Pruefungsform.PROJEKT,
                note=1.7,
            )
        )

        modul = repository.studium.modul_finden("OOP")
        self.assertIsNotNone(modul)
        self.assertEqual("Objektorientierte Programmierung und Design", modul.kursname)
        self.assertEqual(10, modul.ects)
        self.assertEqual(Pruefungsform.PROJEKT, modul.pruefungsleistung.pruefungsform)
        self.assertEqual(1.7, modul.aktuelle_note)

    def test_modul_kann_beim_hinzufuegen_mit_note_angelegt_werden(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        service: StudiumBearbeitenUseCase = StudiumBearbeitenService(repository)

        service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )

        modul = repository.studium.modul_finden("OOP")
        self.assertEqual(2.3, modul.aktuelle_note)

    def test_analyse_service_implementiert_frontend_port(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseUseCase = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual("Software Engineering", dashboard_daten.studiengang)
        self.assertEqual(1, len(dashboard_daten.module))
        self.assertEqual("Portfolio", dashboard_daten.module[0].pruefungsform)

    def test_analyse_service_berechnet_ects_kennzahlen(self) -> None:
        repository = InMemoryStudiumRepository(self._studium(gesamt_ects=18))
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseUseCase = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )
        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="MATHE",
                kursname="Mathematik Grundlagen",
                ects=5,
                pruefungsform=None,
                ist_anerkannt=True,
            )
        )
        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="DB",
                kursname="Datenbanken",
                ects=5,
                pruefungsform=Pruefungsform.KLAUSUR,
            )
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(15, dashboard_daten.erreichte_ects)
        self.assertEqual(3, dashboard_daten.offene_ects)
        self.assertEqual(20, dashboard_daten.geplante_ects)
        self.assertEqual(0, dashboard_daten.ungeplante_ects)
        self.assertEqual(83.33, dashboard_daten.fortschritt_prozent)

    def test_analyse_service_unterscheidet_offene_und_ungeplante_ects(self) -> None:
        repository = InMemoryStudiumRepository(self._studium(gesamt_ects=30))
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseUseCase = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )
        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="DB",
                kursname="Datenbanken",
                ects=5,
                pruefungsform=Pruefungsform.KLAUSUR,
            )
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(10, dashboard_daten.erreichte_ects)
        self.assertEqual(20, dashboard_daten.offene_ects)
        self.assertEqual(15, dashboard_daten.geplante_ects)
        self.assertEqual(15, dashboard_daten.ungeplante_ects)

    def test_analyse_service_liefert_pruefungsversuche_fuer_frontend(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseUseCase = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )
        bearbeiten_service.modul_bearbeiten(
            ModulBearbeitenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=5.0,
            )
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )
        modul_daten = dashboard_daten.module[0]

        self.assertIsNone(modul_daten.note)
        self.assertEqual(1, len(modul_daten.versuche))
        self.assertEqual(5.0, modul_daten.versuche[-1].note)
        self.assertFalse(modul_daten.versuche[-1].ist_bestanden)

    def test_anerkanntes_modul_kann_ohne_pruefungsform_angelegt_werden(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        bearbeiten_service: StudiumBearbeitenUseCase = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseUseCase = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="MATHE",
                kursname="Mathematik Grundlagen",
                ects=5,
                pruefungsform=None,
                ist_anerkannt=True,
            )
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(5, dashboard_daten.erreichte_ects)
        self.assertIsNone(dashboard_daten.module[0].pruefungsform)

    def _studium(self, gesamt_ects: int = 180) -> Studium:
        return Studium(
            studiengang="Software Engineering",
            startdatum=date(2025, 1, 1),
            zieldatum=date(2028, 1, 1),
            gesamt_ects=gesamt_ects,
            ziel_notendurchschnitt=2.0,
        )


if __name__ == "__main__":
    unittest.main()
