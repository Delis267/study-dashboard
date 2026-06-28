import tempfile
import unittest
from datetime import date
from pathlib import Path

from application.dtos.studium_bearbeiten_requests import (
    ModulBearbeitenRequest,
    ModulHinzufuegenRequest,
)
from application.use_cases.studien_analyse_service import StudienAnalyseService
from application.use_cases.studium_bearbeiten_service import StudiumBearbeitenService
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.studium import Studium
from infrastructure.persistence.json_studium_repository import JsonStudiumRepository


class StudienDashboardIntegrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.dateiname = Path(self._tempdir.name) / "studium.json"
        self.repository = JsonStudiumRepository(self.dateiname)
        self.repository.speichern(self._studium())
        self.bearbeiten_service = StudiumBearbeitenService(self.repository)
        self.analyse_service = StudienAnalyseService(self.repository)

    def tearDown(self) -> None:
        self._tempdir.cleanup()

    def test_modul_hinzufuegen_ist_im_dashboard_sichtbar(self) -> None:
        self.bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )

        dashboard_daten = self.analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(1, len(dashboard_daten.module))
        self.assertEqual("OOP", dashboard_daten.module[0].kurs_id)
        self.assertEqual(ModulStatus.OFFEN, dashboard_daten.module[0].status)
        self.assertEqual("Portfolio", dashboard_daten.module[0].pruefungsform)

    def test_pruefungsversuche_werden_gespeichert_und_ausgewertet(self) -> None:
        self.bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )
        self.bearbeiten_service.modul_bearbeiten(
            ModulBearbeitenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=5.0,
            )
        )
        self.bearbeiten_service.modul_bearbeiten(
            ModulBearbeitenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )

        dashboard_daten = self.analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )
        modul = dashboard_daten.module[0]

        self.assertEqual(ModulStatus.FERTIG, modul.status)
        self.assertEqual(2.3, modul.note)
        self.assertEqual(2, len(modul.versuche))
        self.assertFalse(modul.versuche[0].ist_bestanden)
        self.assertTrue(modul.versuche[1].ist_bestanden)
        self.assertEqual(10, dashboard_daten.erreichte_ects)
        self.assertEqual(2.3, dashboard_daten.notendurchschnitt)

    def test_anerkanntes_modul_zaehlt_als_erreicht_aber_nicht_in_den_notenschnitt(self) -> None:
        self.bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=10,
                pruefungsform=Pruefungsform.PORTFOLIO,
                note=2.3,
            )
        )
        self.bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="MATHE",
                kursname="Mathematik Grundlagen",
                ects=5,
                pruefungsform=None,
                ist_anerkannt=True,
            )
        )

        dashboard_daten = self.analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )

        self.assertEqual(15, dashboard_daten.erreichte_ects)
        self.assertEqual(2.3, dashboard_daten.notendurchschnitt)
        self.assertEqual(5, dashboard_daten.ects_nach_status[ModulStatus.ANERKANNT])
        self.assertIsNone(dashboard_daten.module[1].pruefungsform)

    def test_modul_loeschen_entfernt_es_aus_der_persistierten_ansicht(self) -> None:
        self.bearbeiten_service.modul_hinzufuegen(
            ModulHinzufuegenRequest(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsform=Pruefungsform.PORTFOLIO,
            )
        )

        self.bearbeiten_service.modul_loeschen("OOP")

        dashboard_daten = self.analyse_service.dashboard_daten_abrufen(
            stichtag=date(2025, 7, 1)
        )
        self.assertEqual([], dashboard_daten.module)

    def _studium(self) -> Studium:
        return Studium(
            studiengang="Software Engineering",
            startdatum=date(2025, 1, 1),
            zieldatum=date(2028, 1, 1),
            gesamt_ects=20,
            ziel_notendurchschnitt=2.0,
        )


if __name__ == "__main__":
    unittest.main()
