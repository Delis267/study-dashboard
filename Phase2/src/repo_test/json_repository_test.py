import json
from datetime import date
from pathlib import Path

from oo_test.modul import Modul
from oo_test.modul_status import ModulStatus
from oo_test.pruefungsform import Pruefungsform
from oo_test.pruefungsleistung import Pruefungsleistung
from oo_test.studium import Studium

class JsonStudiumRepository:
    def __init__(self, dateiname: str | Path) -> None:
        self.dateiname = Path(dateiname)
        self.dateiname.parent.mkdir(parents=True, exist_ok=True)

    def speichern(self, studium: Studium) -> None:
        '''Speichert das Studium als JSON-Datei und überschreibt die bestehende Datei.'''
        daten = {
            "studiengang": studium.studiengang,
            "startdatum": studium.startdatum.isoformat(),
            "zieldatum": studium.zieldatum.isoformat(),
            "gesamt_ects": studium.gesamt_ects,
            "ziel_notendurchschnitt": studium.ziel_notendurchschnitt,
            "module": [
                {
                    "kurs_id": modul.kurs_id,
                    "kursname": modul.kursname,
                    "ects": modul.ects,
                    "status": modul.status.name,
                    "pruefungsform": modul.pruefungsleistung.pruefungsform.name,
                    "noten": [
                        versuch.note
                        for versuch in modul.pruefungsleistung.versuche
                    ],
                }
                for modul in studium.module
            ],
        }

        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4, ensure_ascii=False)

    def laden(self) -> Studium:
        '''Lädt das Studium aus der JSON-Datei.'''
        with open(self.dateiname, "r", encoding="utf-8") as datei:
            daten = json.load(datei)

        studium = Studium(
            studiengang=daten["studiengang"],
            startdatum=date.fromisoformat(daten["startdatum"]),
            zieldatum=date.fromisoformat(daten["zieldatum"]),
            gesamt_ects=daten["gesamt_ects"],
            ziel_notendurchschnitt=daten["ziel_notendurchschnitt"],
        )

        for modul_daten in daten["module"]:
            modul = Modul(
                kurs_id=modul_daten["kurs_id"],
                kursname=modul_daten["kursname"],
                ects=modul_daten["ects"],
                pruefungsleistung=Pruefungsleistung(
                    Pruefungsform[modul_daten["pruefungsform"]]
                ),
            )

            for note in modul_daten["noten"]:
                modul.note_eintragen(note)

            modul.status = ModulStatus[modul_daten["status"]]
            studium.modul_hinzufuegen(modul)

        return studium


