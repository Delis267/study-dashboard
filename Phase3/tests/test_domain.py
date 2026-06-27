import unittest
from datetime import date

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.pruefungsversuch import Pruefungsversuch
from domain.studium import Studium


class DomainTest(unittest.TestCase):
    def test_pruefungsversuch_erlaubt_nur_fachliche_notenwerte(self) -> None:
        Pruefungsversuch(1.0)
        Pruefungsversuch(4.0)
        Pruefungsversuch(5.0)

        for note in (4.3, 5.7, 6.0):
            with self.subTest(note=note):
                with self.assertRaises(ValueError):
                    Pruefungsversuch(note)

    def test_pruefungsleistung_begrenzt_versuche_und_stoppt_nach_bestanden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(2.3)

        self.assertTrue(pruefungsleistung.ist_bestanden)
        self.assertEqual(2, pruefungsleistung.versuche_anzahl)
        with self.assertRaises(ValueError):
            pruefungsleistung.versuch_eintragen(1.7)

    def test_modul_status_folgt_pruefungsleistung(self) -> None:
        modul = Modul(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsleistung=Pruefungsleistung(Pruefungsform.PORTFOLIO),
        )

        self.assertEqual(ModulStatus.OFFEN, modul.status)

        modul.note_eintragen(5.0)
        self.assertEqual(ModulStatus.IN_ARBEIT, modul.status)

        modul.note_eintragen(2.3)
        self.assertEqual(ModulStatus.FERTIG, modul.status)
        self.assertEqual(2.3, modul.aktuelle_note)

    def test_anerkanntes_modul_hat_keine_pruefungsleistung_und_keine_note(self) -> None:
        modul = Modul(
            kurs_id="MATHE",
            kursname="Mathematik Grundlagen",
            ects=5,
            pruefungsleistung=None,
            status=ModulStatus.ANERKANNT,
        )

        self.assertIsNone(modul.pruefungsleistung)
        self.assertIsNone(modul.aktuelle_note)
        with self.assertRaises(ValueError):
            modul.note_eintragen(2.0)

    def test_studium_berechnet_ects_notenschnitt_velocity_und_prognose(self) -> None:
        studium = Studium(
            studiengang="Software Engineering",
            startdatum=date(2025, 1, 1),
            zieldatum=date(2028, 1, 1),
            gesamt_ects=20,
            ziel_notendurchschnitt=2.5,
        )
        oop = Modul(
            kurs_id="OOP",
            kursname="Objektorientierte Programmierung",
            ects=5,
            pruefungsleistung=Pruefungsleistung(Pruefungsform.PORTFOLIO),
        )
        datenbanken = Modul(
            kurs_id="DB",
            kursname="Datenbanken",
            ects=5,
            pruefungsleistung=Pruefungsleistung(Pruefungsform.KLAUSUR),
        )
        anerkannt = Modul(
            kurs_id="MATHE",
            kursname="Mathematik Grundlagen",
            ects=5,
            pruefungsleistung=None,
            status=ModulStatus.ANERKANNT,
        )

        studium.modul_hinzufuegen(oop)
        studium.modul_hinzufuegen(datenbanken)
        studium.modul_hinzufuegen(anerkannt)
        oop.note_eintragen(2.0)
        datenbanken.note_eintragen(3.0)

        self.assertEqual(15, studium.erreichte_ects)
        self.assertEqual(10, studium.eigenleistung_ects)
        self.assertEqual(5, studium.offene_ects)
        self.assertEqual(2.5, studium.gewichteter_notendurchschnitt)
        self.assertTrue(studium.ziel_notendurchschnitt_erreicht)
        self.assertEqual(5, studium.ects_fuer_status(ModulStatus.ANERKANNT))
        self.assertEqual(10, studium.ects_fuer_status(ModulStatus.FERTIG))
        self.assertEqual(
            15,
            studium.ects_fuer_status(ModulStatus.FERTIG, ModulStatus.ANERKANNT),
        )
        with self.assertRaises(ValueError):
            studium.ects_fuer_status()
        self.assertGreater(studium.velocity(date(2025, 7, 1)), 0)
        self.assertIsNotNone(studium.prognostiziertes_ende(date(2025, 7, 1)))


if __name__ == "__main__":
    unittest.main()
