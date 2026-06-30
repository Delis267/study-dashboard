# Installationsanleitung Studien-Dashboard
GitHub-Link: https://github.com/Delis267/study-dashboard

## Hinweise zur Projektstruktur

Jede Projektphase besitzt ein eigenes Hauptverzeichnis: `\Phase1`, `\Phase2` und `\Phase3` mit folgenden Aufbau:
- Eine `README.md` zur Orientierung.
- Ein Startskript zum einfachen Starten der Testprogramme `run_phase1.py`, `run_phase2.py` und `run_phase3.py`.
- Im Ordner `src` befindet sich der jeweilige Python-Quellcode, der gestartet wird.
- Im Ordner `docs` befinden sich Dokumentationsartefakte der Abgaben.

## Anwendung aus Phase3 starten

Nachdem das Projekt heruntergeladen wurde befindet sich die fertige Anwendung im Ordner `Phase3`.  \
Zum Starten bitte folgenden Befehl im Ordner `"study-dashboard\Phase3"` ausführen: \
`python run_phase3.py`

Alternativer Start über das Bootstrap-Modul (Composition-Root) im Ordner `"study-dashboard\Phase3\src"`. \
`python -m bootstrap.main`

Danach öffnet sich die Tkinter-Oberfläche des Studien-Dashboards. Die Anwendung lädt die Beispieldaten aus: `Phase3\src\data\studium.json`

## Hinweise zur Bedienung

- Ein neues Modul wird über die Schaltfläche `Neues Modul hinzufügen` angelegt.
- Ein vorhandenes Modul kann per Doppelklick in der Tabelle bearbeitet oder gelöscht werden.
- Die Modultabelle lässt sich mit Klick auf den Tabellenkopf sortieren.
- Studiumsgrunddaten können in der JSON-Datei manuell verändert werden
- Die Anwendung untersützt keinen Darkmode

