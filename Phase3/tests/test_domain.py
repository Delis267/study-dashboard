import unittest
from datetime import date

from domain.modul import Modul
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsleistung import Pruefungsleistung
from domain.pruefungsversuch import Pruefungsversuch
from domain.studium import Studium


class PruefungsversuchTest(unittest.TestCase):
    def test_note_fachlich_zulaessig(self) -> None:
        Pruefungsversuch(1.0)
        Pruefungsversuch(4.0)
        Pruefungsversuch(5.0)

    def test_note_4_3_ist_fachlich_nicht_zulaessig(self) -> None:
        with self.assertRaises(ValueError):
            Pruefungsversuch(4.3)

    def test_note_5_7_ist_fachlich_nicht_zulaessig(self) -> None:
        with self.assertRaises(ValueError):
            Pruefungsversuch(5.7)

    def test_note_4_0_gilt_als_bestanden(self) -> None:
        versuch = Pruefungsversuch(4.0)

        self.assertTrue(versuch.ist_bestanden)

    def test_note_5_0_gilt_als_nicht_bestanden(self) -> None:
        versuch = Pruefungsversuch(5.0)

        self.assertFalse(versuch.ist_bestanden)


class PruefungsleistungTest(unittest.TestCase):
    def test_neue_pruefungsleistung_hat_keinen_letzten_versuch(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        self.assertIsNone(pruefungsleistung.letzter_versuch)

    def test_neue_pruefungsleistung_ist_nicht_bestanden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        self.assertFalse(pruefungsleistung.ist_bestanden)

    def test_versuch_eintragen_erhoeht_versuchsanzahl(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(5.0)

        self.assertEqual(1, pruefungsleistung.versuche_anzahl)

    def test_letzter_versuch_ist_der_zuletzt_eingetragene_versuch(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(3.0)

        self.assertEqual(3.0, pruefungsleistung.letzter_versuch.note)

    def test_versuche_werden_nur_als_tuple_herausgegeben(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        self.assertIsInstance(pruefungsleistung.versuche, tuple)

    def test_bestandener_letzter_versuch_markiert_pruefungsleistung_als_bestanden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(2.0)

        self.assertTrue(pruefungsleistung.ist_bestanden)

    def test_nicht_bestandener_letzter_versuch_markiert_pruefungsleistung_als_nicht_bestanden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(5.0)

        self.assertFalse(pruefungsleistung.ist_bestanden)

    def test_nach_bestandener_pruefung_darf_kein_weiterer_versuch_eingetragen_werden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)
        pruefungsleistung.versuch_eintragen(2.0)

        with self.assertRaises(ValueError):
            pruefungsleistung.versuch_eintragen(1.7)

    def test_nach_drei_nicht_bestandenen_versuchen_ist_pruefung_endgueltig_nicht_bestanden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(5.0)

        self.assertTrue(pruefungsleistung.ist_endgueltig_nicht_bestanden)

    def test_nach_drei_versuchen_darf_kein_vierter_versuch_eingetragen_werden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)
        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(5.0)
        pruefungsleistung.versuch_eintragen(5.0)

        with self.assertRaises(ValueError):
            pruefungsleistung.versuch_eintragen(5.0)

    def test_pruefungsform_kann_geaendert_werden(self) -> None:
        pruefungsleistung = Pruefungsleistung(Pruefungsform.KLAUSUR)

        pruefungsleistung.pruefungsform_aendern(Pruefungsform.PORTFOLIO)

        self.assertEqual(Pruefungsform.PORTFOLIO, pruefungsleistung.pruefungsform)

    def test_pruefungsleistung_braucht_pruefungsform(self) -> None:
        with self.assertRaises(ValueError):
            Pruefungsleistung(None)


class ModulTest(unittest.TestCase):
    def test_modul_ohne_kurs_id_ist_ungueltig(self) -> None:
        with self.assertRaises(ValueError):
            self._modul(kurs_id=" ")

    def test_modul_ohne_kursname_ist_ungueltig(self) -> None:
        with self.assertRaises(ValueError):
            self._modul(kursname=" ")

    def test_modul_mit_null_ects_ist_ungueltig(self) -> None:
        with self.assertRaises(ValueError):
            self._modul(ects=0)

    def test_regulaeres_modul_wird_mit_pruefungsleistung_erzeugt(self) -> None:
        modul = self._modul()

        self.assertIsNotNone(modul.pruefungsleistung)

    def test_modul_ohne_pruefungsleistung_ist_anerkannt(self) -> None:
        modul = self._anerkanntes_modul()

        self.assertEqual(ModulStatus.ANERKANNT, modul.status)

    def test_neues_modul_ist_offen(self) -> None:
        modul = self._modul()

        self.assertEqual(ModulStatus.OFFEN, modul.status)

    def test_nicht_bestandener_versuch_setzt_modul_in_arbeit(self) -> None:
        modul = self._modul()

        modul.note_eintragen(5.0)

        self.assertEqual(ModulStatus.IN_ARBEIT, modul.status)

    def test_bestandener_versuch_setzt_modul_auf_fertig(self) -> None:
        modul = self._modul()

        modul.note_eintragen(2.0)

        self.assertEqual(ModulStatus.FERTIG, modul.status)

    def test_aktuelle_note_ist_none_wenn_noch_kein_versuch_existiert(self) -> None:
        modul = self._modul()

        self.assertIsNone(modul.aktuelle_note)

    def test_aktuelle_note_ist_none_wenn_letzter_versuch_nicht_bestanden_ist(self) -> None:
        modul = self._modul()

        modul.note_eintragen(5.0)

        self.assertIsNone(modul.aktuelle_note)

    def test_aktuelle_note_ist_note_des_bestandenen_letzten_versuchs(self) -> None:
        modul = self._modul()

        modul.note_eintragen(5.0)
        modul.note_eintragen(2.3)

        self.assertEqual(2.3, modul.aktuelle_note)

    def test_kursname_kann_geaendert_werden(self) -> None:
        modul = self._modul()

        modul.basisdaten_aendern(kursname="Objektorientierte Programmierung und Design")

        self.assertEqual("Objektorientierte Programmierung und Design", modul.kursname)

    def test_leerer_kursname_darf_nicht_gesetzt_werden(self) -> None:
        modul = self._modul()

        with self.assertRaises(ValueError):
            modul.basisdaten_aendern(kursname=" ")

    def test_ects_koennen_geaendert_werden(self) -> None:
        modul = self._modul()

        modul.basisdaten_aendern(ects=10)

        self.assertEqual(10, modul.ects)

    def test_negative_ects_duerfen_nicht_gesetzt_werden(self) -> None:
        modul = self._modul()

        with self.assertRaises(ValueError):
            modul.basisdaten_aendern(ects=-1)

    def test_pruefungsform_kann_geaendert_werden(self) -> None:
        modul = self._modul()

        modul.pruefungsform_aendern(Pruefungsform.PROJEKT)

        self.assertEqual(Pruefungsform.PROJEKT, modul.pruefungsleistung.pruefungsform)

    def test_anerkanntes_modul_hat_keine_pruefungsleistung(self) -> None:
        modul = self._anerkanntes_modul()

        self.assertIsNone(modul.pruefungsleistung)

    def test_anerkanntes_modul_hat_keine_aktuelle_note(self) -> None:
        modul = self._anerkanntes_modul()

        self.assertIsNone(modul.aktuelle_note)

    def test_fuer_anerkanntes_modul_darf_keine_note_eingetragen_werden(self) -> None:
        modul = self._anerkanntes_modul()

        with self.assertRaises(ValueError):
            modul.note_eintragen(2.0)

    def test_fuer_anerkanntes_modul_darf_pruefungsform_nicht_geaendert_werden(self) -> None:
        modul = self._anerkanntes_modul()

        with self.assertRaises(ValueError):
            modul.pruefungsform_aendern(Pruefungsform.PROJEKT)

    def test_modul_ohne_versuche_kann_anerkannt_werden(self) -> None:
        modul = self._modul()

        modul.anerkennen()

        self.assertEqual(ModulStatus.ANERKANNT, modul.status)

    def test_anerkennung_entfernt_pruefungsleistung(self) -> None:
        modul = self._modul()

        modul.anerkennen()

        self.assertIsNone(modul.pruefungsleistung)

    def test_modul_mit_pruefungsversuch_kann_nicht_anerkannt_werden(self) -> None:
        modul = self._modul()
        modul.note_eintragen(5.0)

        with self.assertRaises(ValueError):
            modul.anerkennen()

    def _modul(
        self,
        kurs_id: str = "OOP",
        kursname: str = "Objektorientierte Programmierung",
        ects: int = 5,
    ) -> Modul:
        return Modul.regulaer(
            kurs_id=kurs_id,
            kursname=kursname,
            ects=ects,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )

    def _anerkanntes_modul(self) -> Modul:
        return Modul.anerkannt(
            kurs_id="MATHE",
            kursname="Mathematik Grundlagen",
            ects=5,
        )


class StudiumTest(unittest.TestCase):
    def test_studium_ohne_studiengang_ist_ungueltig(self) -> None:
        with self.assertRaises(ValueError):
            self._studium(studiengang=" ")

    def test_studium_muss_vor_zieldatum_starten(self) -> None:
        with self.assertRaises(ValueError):
            self._studium(startdatum=date(2028, 1, 1), zieldatum=date(2028, 1, 1))

    def test_studium_braucht_positive_gesamt_ects(self) -> None:
        with self.assertRaises(ValueError):
            self._studium(gesamt_ects=0)

    def test_ziel_notendurchschnitt_darf_nicht_besser_als_1_0_sein(self) -> None:
        with self.assertRaises(ValueError):
            self._studium(ziel_notendurchschnitt=0.9)

    def test_ziel_notendurchschnitt_darf_nicht_schlechter_als_4_0_sein(self) -> None:
        with self.assertRaises(ValueError):
            self._studium(ziel_notendurchschnitt=4.1)

    def test_modul_hinzufuegen_speichert_modul_im_studium(self) -> None:
        studium = self._studium()
        modul = self._modul(kurs_id="OOP")

        studium.modul_hinzufuegen(modul)

        self.assertIs(modul, studium.module[0])

    def test_modul_finden_liefert_modul_mit_passender_kurs_id(self) -> None:
        studium = self._studium_mit_oop()

        modul = studium.modul_finden("OOP")

        self.assertEqual("Objektorientierte Programmierung", modul.kursname)

    def test_modul_finden_liefert_none_fuer_unbekannte_kurs_id(self) -> None:
        studium = self._studium_mit_oop()

        self.assertIsNone(studium.modul_finden("DB"))

    def test_module_mit_gleicher_kurs_id_duerfen_nicht_doppelt_hinzugefuegt_werden(self) -> None:
        studium = self._studium_mit_oop()

        with self.assertRaises(ValueError):
            studium.modul_hinzufuegen(self._modul(kurs_id="OOP"))

    def test_modul_entfernen_loescht_modul_aus_studium(self) -> None:
        studium = self._studium_mit_oop()

        studium.modul_entfernen("OOP")

        self.assertEqual([], studium.module)

    def test_unbekanntes_modul_kann_nicht_entfernt_werden(self) -> None:
        studium = self._studium()

        with self.assertRaises(ValueError):
            studium.modul_entfernen("OOP")

    def test_ects_fuer_status_braucht_mindestens_einen_status(self) -> None:
        studium = self._studium()

        with self.assertRaises(ValueError):
            studium.ects_fuer_status()

    def test_ects_fuer_status_summiert_nur_passende_module(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(10, studium.ects_fuer_status(ModulStatus.FERTIG))

    def test_ects_fuer_mehrere_status_werden_zusammen_summiert(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(15, studium.ects_fuer_status(ModulStatus.FERTIG, ModulStatus.ANERKANNT))

    def test_erreichte_ects_enthalten_fertige_und_anerkannte_module(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(15, studium.erreichte_ects)

    def test_eigenleistung_ects_enthalten_nur_fertige_module(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(10, studium.eigenleistung_ects)

    def test_offene_ects_sind_ziel_minus_erreichte_ects(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul(gesamt_ects=20)

        self.assertEqual(5, studium.offene_ects)

    def test_offene_ects_werden_nicht_negativ(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul(gesamt_ects=10)

        self.assertEqual(0, studium.offene_ects)

    def test_fortschritt_prozent_wird_auf_zwei_nachkommastellen_gerundet(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul(gesamt_ects=18)

        self.assertEqual(83.33, studium.fortschritt_prozent)

    def test_notendurchschnitt_ist_none_wenn_keine_note_vorliegt(self) -> None:
        studium = self._studium()

        self.assertIsNone(studium.gewichteter_notendurchschnitt)

    def test_notendurchschnitt_ignoriert_anerkannte_module(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(2.3, studium.gewichteter_notendurchschnitt)

    def test_notendurchschnitt_wird_mit_ects_gewichtet(self) -> None:
        studium = self._studium()
        oop = self._bestandener_modul("OOP", 5, 2.0)
        datenbanken = self._bestandener_modul("DB", 10, 3.0)
        studium.modul_hinzufuegen(oop)
        studium.modul_hinzufuegen(datenbanken)

        self.assertEqual(2.67, studium.gewichteter_notendurchschnitt)

    def test_ziel_notendurchschnitt_ist_unbekannt_wenn_noch_keine_note_vorliegt(self) -> None:
        studium = self._studium()

        self.assertIsNone(studium.ziel_notendurchschnitt_erreicht)

    def test_ziel_notendurchschnitt_ist_erreicht_wenn_schnitt_besser_oder_gleich_ziel_ist(self) -> None:
        studium = self._studium(ziel_notendurchschnitt=2.3)
        studium.modul_hinzufuegen(self._bestandener_modul("OOP", 5, 2.3))

        self.assertTrue(studium.ziel_notendurchschnitt_erreicht)

    def test_ziel_notendurchschnitt_ist_nicht_erreicht_wenn_schnitt_schlechter_als_ziel_ist(self) -> None:
        studium = self._studium(ziel_notendurchschnitt=2.0)
        studium.modul_hinzufuegen(self._bestandener_modul("OOP", 5, 2.3))

        self.assertFalse(studium.ziel_notendurchschnitt_erreicht)

    def test_ziel_velocity_berechnet_noetige_ects_pro_monat_bis_zieldatum(self) -> None:
        studium = self._studium(gesamt_ects=180)

        self.assertEqual(5.0, studium.ziel_velocity)

    def test_velocity_ist_null_am_studienstart(self) -> None:
        studium = self._studium()

        self.assertEqual(0.0, studium.velocity(date(2025, 1, 1)))

    def test_velocity_nutzt_nur_fertige_eigenleistung_ects(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul()

        self.assertEqual(1.68, studium.velocity(date(2025, 7, 1)))

    def test_velocity_darf_nicht_vor_studienstart_berechnet_werden(self) -> None:
        studium = self._studium()

        with self.assertRaises(ValueError):
            studium.velocity(date(2024, 12, 31))

    def test_prognose_ist_none_wenn_keine_velocity_vorliegt(self) -> None:
        studium = self._studium()

        self.assertIsNone(studium.prognostiziertes_ende(date(2025, 7, 1)))

    def test_prognose_berechnet_abschlussdatum_aus_offenen_ects_und_velocity(self) -> None:
        studium = self._studium_mit_fertigem_und_anerkanntem_modul(gesamt_ects=20)

        self.assertEqual(date(2025, 9, 30), studium.prognostiziertes_ende(date(2025, 7, 1)))

    def _studium(
        self,
        studiengang: str = "Software Engineering",
        startdatum: date = date(2025, 1, 1),
        zieldatum: date = date(2028, 1, 1),
        gesamt_ects: int = 180,
        ziel_notendurchschnitt: float = 2.5,
    ) -> Studium:
        return Studium(
            studiengang=studiengang,
            startdatum=startdatum,
            zieldatum=zieldatum,
            gesamt_ects=gesamt_ects,
            ziel_notendurchschnitt=ziel_notendurchschnitt,
        )

    def _studium_mit_oop(self) -> Studium:
        studium = self._studium()
        studium.modul_hinzufuegen(self._modul(kurs_id="OOP"))
        return studium

    def _studium_mit_fertigem_und_anerkanntem_modul(
        self,
        gesamt_ects: int = 20,
    ) -> Studium:
        studium = self._studium(gesamt_ects=gesamt_ects)
        studium.modul_hinzufuegen(self._bestandener_modul("OOP", 10, 2.3))
        studium.modul_hinzufuegen(self._anerkanntes_modul("MATHE", 5))
        studium.modul_hinzufuegen(self._modul(kurs_id="DB", ects=5))
        return studium

    def _modul(
        self,
        kurs_id: str,
        ects: int = 5,
    ) -> Modul:
        return Modul.regulaer(
            kurs_id=kurs_id,
            kursname="Objektorientierte Programmierung",
            ects=ects,
            pruefungsform=Pruefungsform.PORTFOLIO,
        )

    def _bestandener_modul(
        self,
        kurs_id: str,
        ects: int,
        note: float,
    ) -> Modul:
        modul = self._modul(kurs_id=kurs_id, ects=ects)
        modul.note_eintragen(note)
        return modul

    def _anerkanntes_modul(self, kurs_id: str, ects: int) -> Modul:
        return Modul.anerkannt(
            kurs_id=kurs_id,
            kursname="Anerkanntes Modul",
            ects=ects,
        )


if __name__ == "__main__":
    unittest.main()
