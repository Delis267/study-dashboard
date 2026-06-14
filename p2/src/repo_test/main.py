from datetime import date
from pathlib import Path

from oo_test.modul import Modul
from oo_test.pruefungsform import Pruefungsform
from oo_test.pruefungsleistung import Pruefungsleistung
from oo_test.studium import Studium
from .json_repository_test import JsonStudiumRepository

studium = Studium(
    studiengang="Software Engineering",
    startdatum=date(2025, 1, 1),
    zieldatum=date(2028, 1, 1),
    gesamt_ects=10,
    ziel_notendurchschnitt=2.0,
)

modul_eins = Modul(
    kurs_id="k1",
    kursname="Objektorientierte Programmierung mit Python",
    ects=5,
    pruefungsleistung=Pruefungsleistung(Pruefungsform.PORTFOLIO),
)
modul_zwei = Modul(
    kurs_id="k2",
    kursname="Datenstrukturen und Algorithmen",
    ects=5,
    pruefungsleistung=Pruefungsleistung(Pruefungsform.KLAUSUR),
)


repository = JsonStudiumRepository(Path(__file__).resolve().parent / "data" / "studium.json")

print("==== Speichern ====")
studium.modul_hinzufuegen(modul_eins)
studium.modul_hinzufuegen(modul_zwei)
repository.speichern(studium)
studium.status_ausgeben()

print("==== Laden und Noten Einstragen und wieder speichern ====")
geladenes_studium = repository.laden()
geladenes_studium.module[0].note_eintragen(5.0)
geladenes_studium.module[0].note_eintragen(2.3)
geladenes_studium.status_ausgeben()
repository.speichern(geladenes_studium)