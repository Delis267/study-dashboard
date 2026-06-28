import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.studium import Studium
from infrastructure.persistence.json_studium_repository import JsonStudiumRepository


class JsonStudiumRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tempdir = tempfile.TemporaryDirectory()
        self.dateiname = Path(self._tempdir.name) / "studium.json"
        self.repository = JsonStudiumRepository(self.dateiname)

    def tearDown(self) -> None:
        self._tempdir.cleanup()

    def test_speichern_schreibt_studium_basisdaten(self) -> None:
        self.repository.speichern(self._studium())

        gespeicherte_daten = self._gespeicherte_daten()

        self.assertEqual("Software Engineering", gespeicherte_daten["studiengang"])
        self.assertEqual("2025-01-01", gespeicherte_daten["startdatum"])
        self.assertEqual("2028-01-01", gespeicherte_daten["zieldatum"])
        self.assertEqual(20, gespeicherte_daten["gesamt_ects"])
        self.assertEqual(2.0, gespeicherte_daten["ziel_notendurchschnitt"])

    def test_speichern_schreibt_regulaeres_modul_mit_pruefungsform(self) -> None:
        studium = self._studium_mit_oop()

        self.repository.speichern(studium)

        gespeichertes_modul = self._gespeicherte_daten()["module"][0]
        self.assertEqual("OOP", gespeichertes_modul["kurs_id"])
        self.assertEqual(
            "Objektorientierte Programmierung",
            gespeichertes_modul["kursname"],
        )
        self.assertEqual(5, gespeichertes_modul["ects"])
        self.assertEqual(
            "PORTFOLIO",
            gespeichertes_modul["pruefungsleistung"]["pruefungsform"],
        )

    def test_speichern_schreibt_pruefungsversuche(self) -> None:
        studium = self._studium_mit_oop()
        modul = studium.modul_finden("OOP")
        modul.note_eintragen(5.0)
        modul.note_eintragen(2.3)

        self.repository.speichern(studium)

        gespeichertes_modul = self._gespeicherte_daten()["module"][0]
        self.assertEqual(
            [{"note": 5.0}, {"note": 2.3}],
            gespeichertes_modul["pruefungsleistung"]["versuche"],
        )

    def test_speichern_schreibt_anerkanntes_modul_ohne_pruefungsleistung(self) -> None:
        studium = self._studium()
        studium.modul_hinzufuegen(self._anerkanntes_modul())

        self.repository.speichern(studium)

        gespeichertes_modul = self._gespeicherte_daten()["module"][0]
        self.assertIsNone(gespeichertes_modul["pruefungsleistung"])

    def test_speichern_schreibt_keinen_abgeleiteten_status(self) -> None:
        studium = self._studium_mit_oop()
        modul = studium.modul_finden("OOP")
        modul.note_eintragen(2.3)

        self.repository.speichern(studium)

        gespeichertes_modul = self._gespeicherte_daten()["module"][0]
        self.assertNotIn("status", gespeichertes_modul)

    def test_laden_stellt_studium_basisdaten_wieder_her(self) -> None:
        self._json_speichern(self._studium_daten())

        studium = self.repository.laden()

        self.assertEqual("Software Engineering", studium.studiengang)
        self.assertEqual(date(2025, 1, 1), studium.startdatum)
        self.assertEqual(date(2028, 1, 1), studium.zieldatum)
        self.assertEqual(20, studium.gesamt_ects)
        self.assertEqual(2.0, studium.ziel_notendurchschnitt)

    def test_laden_stellt_regulaeres_modul_mit_status_und_note_wieder_her(self) -> None:
        daten = self._studium_daten(
            module=[
                {
                    "kurs_id": "OOP",
                    "kursname": "Objektorientierte Programmierung",
                    "ects": 5,
                    "pruefungsleistung": {
                        "pruefungsform": "PORTFOLIO",
                        "versuche": [{"note": 5.0}, {"note": 2.3}],
                    },
                }
            ]
        )
        self._json_speichern(daten)

        studium = self.repository.laden()

        modul = studium.module[0]
        self.assertEqual("OOP", modul.kurs_id)
        self.assertEqual(ModulStatus.FERTIG, modul.status)
        self.assertEqual(Pruefungsform.PORTFOLIO, modul.pruefungsleistung.pruefungsform)
        self.assertEqual(2.3, modul.aktuelle_note)

    def test_laden_stellt_anerkanntes_modul_ohne_pruefungsleistung_wieder_her(self) -> None:
        daten = self._studium_daten(
            module=[
                {
                    "kurs_id": "MATHE",
                    "kursname": "Mathematik Grundlagen",
                    "ects": 5,
                    "pruefungsleistung": None,
                }
            ]
        )
        self._json_speichern(daten)

        studium = self.repository.laden()

        modul = studium.module[0]
        self.assertEqual("MATHE", modul.kurs_id)
        self.assertEqual(ModulStatus.ANERKANNT, modul.status)
        self.assertIsNone(modul.pruefungsleistung)

    def _studium(self) -> Studium:
        return Studium(
            studiengang="Software Engineering",
            startdatum=date(2025, 1, 1),
            zieldatum=date(2028, 1, 1),
            gesamt_ects=20,
            ziel_notendurchschnitt=2.0,
        )

    def _studium_mit_oop(self) -> Studium:
        studium = self._studium()
        studium.modul_hinzufuegen(self._regulaeres_modul())
        return studium

    def _regulaeres_modul(self) -> Modul:
        return Modul.regulaer(
            "OOP",
            "Objektorientierte Programmierung",
            5,
            Pruefungsform.PORTFOLIO,
        )

    def _anerkanntes_modul(self) -> Modul:
        return Modul.anerkannt(
            "MATHE",
            "Mathematik Grundlagen",
            5,
        )

    def _gespeicherte_daten(self) -> dict:
        with open(self.dateiname, "r", encoding="utf-8") as datei:
            return json.load(datei)

    def _json_speichern(self, daten: dict) -> None:
        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(daten, datei)

    def _studium_daten(self, module: list[dict] | None = None) -> dict:
        return {
            "studiengang": "Software Engineering",
            "startdatum": "2025-01-01",
            "zieldatum": "2028-01-01",
            "gesamt_ects": 20,
            "ziel_notendurchschnitt": 2.0,
            "module": module or [],
        }


if __name__ == "__main__":
    unittest.main()
