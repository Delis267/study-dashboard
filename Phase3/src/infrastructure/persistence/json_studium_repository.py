import json
from datetime import date
from pathlib import Path

from application.ports.studium_repository_port import StudiumRepositoryPort
from domain.modul import Modul
from domain.pruefungsform import Pruefungsform
from domain.studium import Studium


class JsonStudiumRepository(StudiumRepositoryPort):
    def __init__(self, dateiname: str | Path) -> None:
        self.dateiname = Path(dateiname)
        self.dateiname.parent.mkdir(parents=True, exist_ok=True)

    def speichern(self, studium: Studium) -> None:
        daten = {
            "studiengang": studium.studiengang,
            "startdatum": studium.startdatum.isoformat(),
            "zieldatum": studium.zieldatum.isoformat(),
            "gesamt_ects": studium.gesamt_ects,
            "ziel_notendurchschnitt": studium.ziel_notendurchschnitt,
            "module": [self._modul_zu_dict(modul) for modul in studium.module],
        }

        with open(self.dateiname, "w", encoding="utf-8") as datei:
            json.dump(daten, datei, indent=4, ensure_ascii=False)

    def laden(self) -> Studium:
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
            studium.modul_hinzufuegen(self._modul_aus_dict(modul_daten))

        return studium

    def _modul_zu_dict(self, modul: Modul) -> dict:
        pruefungsleistung = None
        if modul.pruefungsleistung is not None:
            pruefungsleistung = {
                "pruefungsform": modul.pruefungsleistung.pruefungsform.name,
                "versuche": [
                    {"note": versuch.note}
                    for versuch in modul.pruefungsleistung.versuche
                ],
            }

        return {
            "kurs_id": modul.kurs_id,
            "kursname": modul.kursname,
            "ects": modul.ects,
            "pruefungsleistung": pruefungsleistung,
        }

    def _modul_aus_dict(self, daten: dict) -> Modul:
        pruefungsleistung_daten = daten["pruefungsleistung"]

        if pruefungsleistung_daten is None:
            return Modul.anerkannt(
                daten["kurs_id"],
                daten["kursname"],
                daten["ects"],
            )

        modul = Modul.regulaer(
            daten["kurs_id"],
            daten["kursname"],
            daten["ects"],
            Pruefungsform[pruefungsleistung_daten["pruefungsform"]],
        )

        for versuch_daten in pruefungsleistung_daten["versuche"]:
            modul.note_eintragen(versuch_daten["note"])

        return modul
