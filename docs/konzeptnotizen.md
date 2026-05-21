# Konzeptnotizen

## Problemstellung

- Im Fernstudium koennen Module flexibel bearbeitet werden.
- Dadurch ist es schwer, den Gesamtfortschritt schnell einzuschaetzen.
- Wichtige Fragen sind:
  - Reichen die bisher erreichten ECTS fuer das 36-Monats-Ziel?
  - Wie viele ECTS fehlen noch?
  - Wie schnell schreitet das Studium aktuell voran?
  - Welche Module sind offen, in Arbeit oder fertig?

## Dashboard-Ziele

- Studienfortschritt uebersichtlich darstellen.
- ECTS-Ziel und bisherige ECTS anzeigen.
- Studiendauer ab Startdatum berechnen.
- Velocity in ECTS pro Monat berechnen.
- Prognose fuer die restliche Studiendauer anzeigen.
- Modulstatus und Noten in einer einfachen Tabelle zeigen.

## Angezeigte Kennzahlen

- abgeschlossene ECTS
- offene ECTS
- bisherige Studiendauer in Monaten
- ECTS pro Monat
- Ziel-ECTS pro Monat
- Prognose der Restmonate
- Restworkload in Stunden
- Notendurchschnitt als spaetere Kennzahl

## Module und Semester

- Module werden nicht fest einem Semester untergeordnet.
- Im IU-Fernstudium koennen Module flexibel gestartet und abgeschlossen werden.
- Ein Modul bekommt deshalb nur ein optionales empfohlenes Semester.
- Der echte Fortschritt wird ueber den Status abgebildet:
  - offen
  - in Arbeit
  - fertig

## Warum CSV?

- CSV ist einfach zu verstehen und mit der Standardbibliothek nutzbar.
- Es wird keine Datenbank und kein externes Paket benoetigt.
- Die Daten koennen leicht in einem Texteditor oder Tabellenprogramm betrachtet werden.
- Fuer Phase 1 reicht CSV als einfacher Machbarkeitstest aus.

## Warum Tkinter?

- Tkinter gehoert zur Python-Standardbibliothek.
- Es muessen keine externen GUI-Pakete installiert werden.
- Fuer einen ersten Test reicht Tkinter aus, um Fenster, Kennzahlen, Fortschrittsbalken und Tabellen darzustellen.

## Hinweis zur Architektur

- In Phase 1 wird noch keine vollstaendige Softwarearchitektur entworfen.
- Es gibt nur einfache Tests und Konzeptmaterialien.
- Die Gesamtarchitektur wird erst in Phase 2 genauer ausgearbeitet.
