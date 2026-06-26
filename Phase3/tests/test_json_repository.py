import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.studium import Studium
from infrastructure.persistence.json_studium_repository import JsonStudiumRepository


class JsonStudiumRepositoryTest(unittest.TestCase):
    def test_speichern_und_laden_erhaelt_domaenenstruktur(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dateiname = Path(tmpdir) / "studium.json"
            repository = JsonStudiumRepository(dateiname)
            studium = Studium(
                studiengang="Software Engineering",
                startdatum=date(2025, 1, 1),
                zieldatum=date(2028, 1, 1),
                gesamt_ects=20,
                ziel_notendurchschnitt=2.0,
            )
            modul = Modul(
                kurs_id="OOP",
                kursname="Objektorientierte Programmierung",
                ects=5,
                pruefungsleistung=Pruefungsleistung(Pruefungsform.PORTFOLIO),
            )
            anerkannt = Modul(
                kurs_id="MATHE",
                kursname="Mathematik Grundlagen",
                ects=5,
                pruefungsleistung=None,
                status=ModulStatus.ANERKANNT,
            )

            studium.modul_hinzufuegen(modul)
            studium.modul_hinzufuegen(anerkannt)
            modul.note_eintragen(5.0)
            modul.note_eintragen(2.3)

            repository.speichern(studium)

            with open(dateiname, "r", encoding="utf-8") as datei:
                gespeicherte_daten = json.load(datei)

            self.assertEqual(
                [{"note": 5.0}, {"note": 2.3}],
                gespeicherte_daten["module"][0]["pruefungsleistung"]["versuche"],
            )
            self.assertIsNone(gespeicherte_daten["module"][1]["pruefungsleistung"])

            geladenes_studium = repository.laden()

            self.assertEqual(2, len(geladenes_studium.module))
            self.assertEqual(ModulStatus.FERTIG, geladenes_studium.module[0].status)
            self.assertEqual(2.3, geladenes_studium.module[0].aktuelle_note)
            self.assertEqual(ModulStatus.ANERKANNT, geladenes_studium.module[1].status)
            self.assertIsNone(geladenes_studium.module[1].pruefungsleistung)


if __name__ == "__main__":
    unittest.main()

