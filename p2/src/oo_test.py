from datetime import date

from p2.src.Modul import Modul
from p2.src.Studium import ModulStatus
from p2.src.Studium import Pruefungsform
from p2.src.Studium import Studium


# Testprogramm
studium = Studium(
    studiengang="Informatik",
    startdatum=date(2025, 1, 1),
    zieldatum=date(2028, 1, 1),
    gesamt_ects=180,
    ziel_notendurchschnitt=2.0
)

modul_eins = Modul(
    kurs_id="K1",
    kursname="Objektorientierte Programmierung mit Python",
    ects=5,
    pruefungsform=Pruefungsform.PORTFOLIO
)

modul_zwei = Modul(
    kurs_id="K2",
    kursname="Datenstrukturen und Algorithmen",
    ects=5,
    pruefungsform=Pruefungsform.KLAUSUR,
    status=ModulStatus.IN_ARBEIT
)

studium.modul_hinzufuegen(modul_eins)
studium.modul_hinzufuegen(modul_zwei)

modul_eins.add_pruefungsleistung(1.7)
modul_zwei.add_pruefungsleistung(6.0)
modul_zwei.add_pruefungsleistung(1.0)

print("Studiengang:", studium.studiengang)
print("Anzahl Module:", len(studium.module))
print()

studium.printModule()

print("Erreichte ECTS:", studium.erreichte_ects)
print("Fortschritt in Prozent:", round(studium.fortschritt_prozent, 2))