import tkinter as tk
from tkinter import ttk


fenster = tk.Tk()
fenster.title("Studien-Dashboard Test")
fenster.geometry("900x650")

ueberschrift = tk.Label(fenster, text="Studien-Dashboard", font=("Arial", 20, "bold"))
ueberschrift.pack(pady=10)

info = tk.Label(fenster, text="Einfacher GUI-Machbarkeitstest mit Tkinter")
info.pack()

kachel_bereich = tk.Frame(fenster)
kachel_bereich.pack(pady=15)

# Vier einfache Kennzahlen-Kacheln
kennzahlen = [
    ("ECTS", "80 / 180"),
    ("Studiendauer", "20 Monate"),
    ("Velocity", "4.0 ECTS/Monat"),
    ("Prognose", "25 Monate offen"),
]

for spalte, kennzahl in enumerate(kennzahlen):
    titel = kennzahl[0]
    wert = kennzahl[1]

    kachel = tk.Frame(kachel_bereich, borderwidth=1, relief="solid", padx=15, pady=10)
    kachel.grid(row=0, column=spalte, padx=8)

    tk.Label(kachel, text=titel, font=("Arial", 10)).pack()
    tk.Label(kachel, text=wert, font=("Arial", 13, "bold")).pack()

fortschritt_label = tk.Label(fenster, text="ECTS-Fortschritt", font=("Arial", 12, "bold"))
fortschritt_label.pack(pady=(15, 5))

fortschritt = ttk.Progressbar(fenster, orient="horizontal", length=600, mode="determinate")
fortschritt["maximum"] = 180
fortschritt["value"] = 80
fortschritt.pack()

tk.Label(fenster, text="80 von 180 ECTS abgeschlossen (44 %)").pack(pady=5)

status = tk.Label(fenster, text="Status: hinter Plan", font=("Arial", 14, "bold"), fg="darkred")
status.pack(pady=10)

modul_label = tk.Label(fenster, text="Moduluebersicht", font=("Arial", 12, "bold"))
modul_label.pack(pady=(10, 5))

sortierung_absteigend = {
    "id": False,
    "titel": False,
    "ects": False,
    "status": False,
    "note": False,
}

tabelle = ttk.Treeview(fenster, columns=("id", "titel", "ects", "status", "note"), show="headings", height=16)
tabelle.heading("id", text="ID", command=lambda: sortiere_tabelle("id"))
tabelle.heading("titel", text="Titel", command=lambda: sortiere_tabelle("titel"))
tabelle.heading("ects", text="ECTS", command=lambda: sortiere_tabelle("ects"))
tabelle.heading("status", text="Status", command=lambda: sortiere_tabelle("status"))
tabelle.heading("note", text="Note", command=lambda: sortiere_tabelle("note"))

tabelle.column("id", width=90)
tabelle.column("titel", width=500)
tabelle.column("ects", width=60)
tabelle.column("status", width=120)
tabelle.column("note", width=80)

beispielmodule = [
    ("IGIS01", "Grundlagen der industriellen Softwaretechnik", "5", "fertig", ""),
    ("DLBWIRTT01", "Einfuehrung in das wissenschaftliche Arbeiten fuer IT und Technik", "5", "fertig", ""),
    ("IREN01", "Requirements Engineering", "5", "fertig", ""),
    ("ISPE01", "Spezifikation", "5", "fertig", ""),
    ("IOBP01", "Grundlagen der objektorientierten Programmierung mit Java", "5", "fertig", ""),
    ("IDBS01", "Datenmodellierung und Datenbanksysteme", "5", "fertig", ""),
    ("DLBCSDSJCL02_D", "Datenstruktur und Java-Klassenbibliothek", "5", "fertig", ""),
    ("DLBKA01", "Kollaboratives Arbeiten", "5", "fertig", ""),
    ("IPWA01-01", "Programmierung von Web-Anwendungsoberflaechen", "5", "fertig", ""),
    ("DLBIADPS01", "Algorithmen, Datenstrukturen und Programmiersprachen", "5", "fertig", ""),
    ("IQSS01", "Qualitaetssicherung im Softwareprozess", "5", "fertig", ""),
    ("IAMG01", "IT-Architekturmanagement", "5", "fertig", ""),
    ("IPWA02-01", "Programmierung von industriellen Informationssystemen mit Java EE", "5", "fertig", ""),
    ("DLBSEPENIT01_D", "Ethik und Nachhaltigkeit in der IT", "5", "fertig", ""),
    ("IPMG01-01", "IT-Projektmanagement", "5", "fertig", ""),
    ("DLBWIWTMAS01", "Techniken und Methoden der agilen Softwareentwicklung", "5", "fertig", ""),
    ("DLBCSEMSE01_D", "Mobile Software Engineering I", "5", "fertig", ""),
    ("ISSE01", "Seminar Software Engineering", "5", "fertig", ""),
    ("IWNFE02", "Projekt Agiles Software Engineering", "5", "in Arbeit", ""),
    ("DLBSEPITI01_D", "IT-Infrastruktur", "5", "in Arbeit", ""),
    ("IWSM01", "IT-Service Management", "5", "in Arbeit", ""),
    ("DLBCSEMSE02_D", "Projekt: Mobile Software Engineering II", "5", "offen", ""),
    ("DLBSEPCP01_D", "Cloud Programming", "5", "offen", ""),
    ("DLBISIC01", "Einfuehrung in Datenschutz und IT-Sicherheit", "5", "offen", ""),
    ("DLBSEPDCOD01_D", "DevOps and Continuous Delivery", "5", "offen", ""),
    ("DLBMIUID01", "Gestaltung und Ergonomie von User Interfaces", "5", "offen", ""),
    ("DLBDSIPWP01_D", "Einfuehrung in die Programmierung mit Python", "5", "offen", ""),
    ("DLBSEPPSD01_D", "Projekt: Software Development", "5", "offen", ""),
    ("WAHL1", "Data Science", "5", "offen", ""),
    ("WAHL2", "OOP-Projekt mit Python", "5", "offen", ""),
    ("WAHL3", "Artificial Intelligence", "5", "offen", ""),
    ("WAHL4", "AI Fluency und generative KI", "5", "offen", ""),
    ("WAHL5", "Einfuehrung in das Internet of Things", "5", "offen", ""),
    ("WAHL6", "Embedded Systems", "5", "offen", ""),
    ("BAK", "Bachelorarbeit", "10", "offen", ""),
]

def sortiere_tabelle(spalte):
    eintraege = []

    for zeile in tabelle.get_children():
        wert = tabelle.set(zeile, spalte)
        eintraege.append((wert, zeile))

    eintraege.sort(reverse=sortierung_absteigend[spalte])

    for index, eintrag in enumerate(eintraege):
        zeile = eintrag[1]
        tabelle.move(zeile, "", index)

    sortierung_absteigend[spalte] = not sortierung_absteigend[spalte]

for modul in beispielmodule:
    tabelle.insert("", "end", values=modul)

tabelle.pack(pady=10)

fenster.mainloop()
