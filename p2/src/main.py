from datetime import date
from modul import Modul
from pruefungsform import Pruefungsform
from studium import Studium

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
    pruefungsform=Pruefungsform.PORTFOLIO,
)
modul_zwei = Modul(
    kurs_id="k2",
    kursname="Datenstrukturen und Algorithmen",
    ects=5,
    pruefungsform=Pruefungsform.KLAUSUR,
)
studium.modul_hinzufuegen(modul_eins)
studium.modul_hinzufuegen(modul_zwei)

print("==== Studiumsbeginn - 2 Module ohne Versuche ====")
studium.status_ausgeben()

modul_eins.note_eintragen(5.0)
print("==== Nach erster Prüfung mit Note 5.0 ====")
studium.status_ausgeben()

modul_eins.note_eintragen(2.3)
print("==== Nach zweiter Prüfung mit Note 2.3 ====")
studium.status_ausgeben()



