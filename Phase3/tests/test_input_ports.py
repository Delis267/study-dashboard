import unittest
from datetime import date

from application.ports.studien_analyse_input_port import StudienAnalyseInputPort
from application.ports.studium_bearbeiten_input_port import StudiumBearbeitenInputPort
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
        service: StudiumBearbeitenInputPort = StudiumBearbeitenService(repository)

        service.modul_hinzufuegen(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )
        service.modul_bearbeiten(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
            note=2.3,
        )

        modul = repository.studium.modul_finden("OOP")
        self.assertIsNotNone(modul)
        self.assertEqual(2.3, modul.aktuelle_note)
        self.assertTrue(repository.wurde_gespeichert)

    def test_modul_kann_ueber_frontend_port_bearbeitet_werden(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        service: StudiumBearbeitenInputPort = StudiumBearbeitenService(repository)

        service.modul_hinzufuegen(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )

        service.modul_bearbeiten(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung und Design",
            ects=10,
            pruefungsform=Pruefungsform.PROJEKT,
            note=1.7,
        )

        modul = repository.studium.modul_finden("OOP")
        self.assertIsNotNone(modul)
        self.assertEqual("Objektorientierte Programmierung und Design", modul.kursname)
        self.assertEqual(10, modul.ects)
        self.assertEqual(Pruefungsform.PROJEKT, modul.pruefungsleistung.pruefungsform)
        self.assertEqual(1.7, modul.aktuelle_note)

    def test_analyse_service_implementiert_frontend_port(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseInputPort = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual("Software Engineering", dashboard_daten.studiengang)
        self.assertEqual(1, len(dashboard_daten.module))
        self.assertEqual("Portfolio", dashboard_daten.module[0].pruefungsform)

    def test_analyse_service_liefert_pruefungsversuche_fuer_frontend(self) -> None:
        repository = InMemoryStudiumRepository(self._studium())
        bearbeiten_service = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseInputPort = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )
        bearbeiten_service.modul_bearbeiten(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsform=Pruefungsform.PORTFOLIO,
            note=5.0,
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
        bearbeiten_service: StudiumBearbeitenInputPort = StudiumBearbeitenService(repository)
        analyse_service: StudienAnalyseInputPort = StudienAnalyseService(repository)

        bearbeiten_service.modul_hinzufuegen(
            kurs_id="MATHE",
            kursname="Mathematik Grundlagen",
            ects=5,
            pruefungsform=None,
        )

        dashboard_daten = analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(5, dashboard_daten.erreichte_ects)
        self.assertIsNone(dashboard_daten.module[0].pruefungsform)

    def _studium(self) -> Studium:
        return Studium(
            studiengang="Software Engineering",
            startdatum=date(2025, 1, 1),
            zieldatum=date(2028, 1, 1),
            gesamt_ects=180,
            ziel_notendurchschnitt=2.0,
        )


if __name__ == "__main__":
    unittest.main()
