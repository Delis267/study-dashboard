import tkinter as tk
from tkinter import ttk


# Beispielmodule fuer den Machbarkeitstest
# Aufbau: Kuerzel, ECTS, Kursname, Pruefungsform, Status, Note
module = [
    ("IGIS01", 5, "Grundlagen der industriellen Softwaretechnik", "Klausur", "anerkannt", ""),
    ("DLBWIRTT01", 5, "Einfuehrung in das wissenschaftliche Arbeiten fuer IT und Technik", "Hausarbeit", "anerkannt", ""),
    ("IREN01", 5, "Requirements Engineering", "Klausur", "fertig", ""),
    ("ISPE01", 5, "Spezifikation", "Klausur", "fertig", ""),
    ("IOBP01", 5, "Grundlagen der objektorientierten Programmierung mit Java", "Klausur", "fertig", ""),
    ("IDBS01", 5, "Datenmodellierung und Datenbanksysteme", "Klausur", "fertig", ""),
    ("DLBCSDSJCL02_D", 5, "Datenstruktur und Java-Klassenbibliothek", "Klausur", "fertig", ""),
    ("DLBKA01", 5, "Kollaboratives Arbeiten", "Portfolio", "fertig", ""),
    ("IPWA01-01", 5, "Programmierung von Web-Anwendungsoberflaechen", "Projekt", "fertig", ""),
    ("DLBIADPS01", 5, "Algorithmen, Datenstrukturen und Programmiersprachen", "Klausur", "fertig", ""),
    ("IQSS01", 5, "Qualitaetssicherung im Softwareprozess", "Klausur", "fertig", ""),
    ("IAMG01", 5, "IT-Architekturmanagement", "Klausur", "fertig", ""),
    ("IPWA02-01", 5, "Programmierung von industriellen Informationssystemen mit Java EE", "Projekt", "fertig", ""),
    ("DLBSEPENIT01_D", 5, "Ethik und Nachhaltigkeit in der IT", "Portfolio", "fertig", ""),
    ("IPMG01-01", 5, "IT-Projektmanagement", "Klausur", "fertig", ""),
    ("DLBWIWTMAS01", 5, "Techniken und Methoden der agilen Softwareentwicklung", "Klausur", "fertig", ""),
    ("DLBCSEMSE01_D", 5, "Mobile Software Engineering I", "Projekt", "in Arbeit", ""),
    ("ISSE01", 5, "Seminar Software Engineering", "Seminar", "offen", ""),
    ("IWNFE02", 5, "Projekt Agiles Software Engineering", "Projekt", "offen", ""),
    ("DLBSEPITI01_D", 5, "IT-Infrastruktur", "Klausur", "offen", ""),
    ("IWSM01", 5, "IT-Service Management", "Klausur", "offen", ""),
    ("DLBCSEMSE02_D", 5, "Projekt: Mobile Software Engineering II", "Projekt", "offen", ""),
    ("DLBSEPCP01_D", 5, "Cloud Programming", "Projekt", "offen", ""),
    ("DLBISIC01", 5, "Einfuehrung in Datenschutz und IT-Sicherheit", "Klausur", "offen", ""),
    ("DLBSEPDCOD01_D", 5, "DevOps and Continuous Delivery", "Projekt", "offen", ""),
    ("DLBMIUID01", 5, "Gestaltung und Ergonomie von User Interfaces", "Portfolio", "offen", ""),
    ("DLBDSIPWP01_D", 5, "Einfuehrung in die Programmierung mit Python", "Portfolio", "offen", ""),
    ("DLBSEPPSD01_D", 5, "Projekt: Software Development", "Projekt", "offen", ""),
    ("WAHL1", 5, "Data Science", "Klausur", "offen", ""),
    ("WAHL2", 5, "OOP-Projekt mit Python", "Portfolio", "offen", ""),
    ("WAHL3", 5, "Artificial Intelligence", "Klausur", "offen", ""),
    ("WAHL4", 5, "AI Fluency und generative KI", "Portfolio", "offen", ""),
    ("WAHL5", 5, "Einfuehrung in das Internet of Things", "Klausur", "offen", ""),
    ("WAHL6", 5, "Embedded Systems", "Klausur", "offen", ""),
    ("BAK", 10, "Bachelorarbeit", "Bachelorarbeit", "offen", ""),
]


def berechne_ects(status):
    summe = 0

    for modul in module:
        if modul[4] == status:
            summe = summe + modul[1]

    return summe


def zeichne_donut(canvas, werte, prozent_fertig):
    gesamt = 0

    for wert in werte:
        gesamt = gesamt + wert[1]

    start_winkel = 90

    for name, ects, farbe in werte:
        winkel = 360 * ects / gesamt
        canvas.create_arc(
            10,
            10,
            170,
            170,
            start=start_winkel,
            extent=winkel,
            fill=farbe,
            outline="white",
            width=2,
        )
        start_winkel = start_winkel + winkel

    # Innerer Kreis macht aus dem Kuchendiagramm ein Donutdiagramm.
    canvas.create_oval(62, 62, 118, 118, fill="white", outline="black", width=2)
    canvas.create_text(90, 84, text=str(prozent_fertig) + "%", font=("Arial", 14, "bold"))
    canvas.create_text(90, 104, text="fertig", font=("Arial", 9))


def sortiere_tabelle(spalte):
    eintraege = []

    for zeile in tabelle.get_children():
        wert = tabelle.set(zeile, spalte)

        if spalte == "ects":
            wert = int(wert)

        eintraege.append((wert, zeile))

    eintraege.sort(reverse=sortierung_absteigend[spalte])

    for index, eintrag in enumerate(eintraege):
        zeile = eintrag[1]
        tabelle.move(zeile, "", index)

    sortierung_absteigend[spalte] = not sortierung_absteigend[spalte]


fenster = tk.Tk()
fenster.title("Studien-Dashboard Test")
fenster.geometry("1050x760")

hauptbereich = tk.Frame(fenster, padx=18, pady=14)
hauptbereich.pack(fill="both", expand=True)

# Oberer Bereich: links Text, rechts Donutdiagramm mit Zahlen
kopfbereich = tk.Frame(hauptbereich, borderwidth=2, relief="solid", padx=12, pady=8)
kopfbereich.pack(fill="x")

info_bereich = tk.Frame(kopfbereich)
info_bereich.grid(row=0, column=0, sticky="w")

tk.Label(info_bereich, text="Study-Dashboard", font=("Arial", 22, "bold")).pack(anchor="w")
tk.Label(info_bereich, text="o B. Sc. Softwareentwicklung", font=("Arial", 11)).pack(anchor="w")
tk.Label(info_bereich, text="o Studienstart: 01.03.2024", font=("Arial", 11)).pack(anchor="w")
tk.Label(info_bereich, text="o Studienziel: 01.03.2027", font=("Arial", 11)).pack(anchor="w")
tk.Label(info_bereich, text="o Hinter Plan", font=("Arial", 11)).pack(anchor="w")

diagramm_bereich = tk.Frame(kopfbereich)
diagramm_bereich.grid(row=0, column=1, sticky="e", padx=(40, 0))

ects_anerkannt = berechne_ects("anerkannt")
ects_fertig = berechne_ects("fertig")
ects_in_arbeit = berechne_ects("in Arbeit")
ects_offen = berechne_ects("offen")
ects_gesamt = ects_anerkannt + ects_fertig + ects_in_arbeit + ects_offen
prozent_fertig = round((ects_anerkannt + ects_fertig) / ects_gesamt * 100)

status_werte = [
    ("anerkannt", ects_anerkannt, "#9ee6a3"),
    ("fertig", ects_fertig, "#19b957"),
    ("in Arbeit", ects_in_arbeit, "#ffd966"),
    ("offen", ects_offen, "#9fd3f5"),
]

donut = tk.Canvas(diagramm_bereich, width=180, height=180)
donut.grid(row=0, column=0, padx=10)
zeichne_donut(donut, status_werte, prozent_fertig)

legende = tk.Frame(diagramm_bereich)
legende.grid(row=0, column=1, sticky="w")

for zeile, status_wert in enumerate(status_werte):
    name = status_wert[0]
    ects = status_wert[1]
    farbe = status_wert[2]

    tk.Label(legende, text="  ", bg=farbe, borderwidth=1, relief="solid").grid(row=zeile, column=0, padx=6, pady=4)
    tk.Label(legende, text=str(ects) + " ECTS " + name).grid(row=zeile, column=1, sticky="w")

kopfbereich.columnconfigure(0, weight=1)

# Mittlerer Bereich: Kennzahlen-Kacheln
kachel_bereich = tk.Frame(hauptbereich)
kachel_bereich.pack(fill="x", pady=12)

kennzahlen = [
    ("ECTS", "80/180", "#aef0b8"),
    ("Notenschnitt", "2.1\nziel 2.0", "#9fd3f5"),
    ("Velocity", "5 ECTS/Monat", "#ffd966"),
    ("Prognose", "Ende: 01.06.2027\n3 Monate\nhinter Plan", "#ffc4c4"),
]

for spalte, kennzahl in enumerate(kennzahlen):
    titel = kennzahl[0]
    wert = kennzahl[1]
    farbe = kennzahl[2]

    kachel = tk.Frame(kachel_bereich, bg=farbe, borderwidth=2, relief="solid", padx=10, pady=8)
    kachel.grid(row=0, column=spalte, sticky="nsew", padx=10)

    tk.Label(kachel, text=titel, bg=farbe, font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(kachel, text=wert, bg=farbe, font=("Arial", 12), justify="left").pack(anchor="w", pady=(4, 0))

    kachel_bereich.columnconfigure(spalte, weight=1)

# Unterer Bereich: Modultabelle
tabellen_bereich = tk.Frame(hauptbereich, borderwidth=2, relief="solid", padx=10, pady=10)
tabellen_bereich.pack(fill="both", expand=True)

sortierung_absteigend = {
    "kuerzel": False,
    "ects": False,
    "kursname": False,
    "pruefungsform": False,
    "status": False,
    "note": False,
}

tabelle = ttk.Treeview(
    tabellen_bereich,
    columns=("kuerzel", "ects", "kursname", "pruefungsform", "status", "note"),
    show="headings",
    height=15,
)

tabelle.heading("kuerzel", text="Kuerzel", command=lambda: sortiere_tabelle("kuerzel"))
tabelle.heading("ects", text="ECTS", command=lambda: sortiere_tabelle("ects"))
tabelle.heading("kursname", text="Kursname", command=lambda: sortiere_tabelle("kursname"))
tabelle.heading("pruefungsform", text="Pruefungsform", command=lambda: sortiere_tabelle("pruefungsform"))
tabelle.heading("status", text="Status", command=lambda: sortiere_tabelle("status"))
tabelle.heading("note", text="Note", command=lambda: sortiere_tabelle("note"))

tabelle.column("kuerzel", width=130)
tabelle.column("ects", width=60)
tabelle.column("kursname", width=420)
tabelle.column("pruefungsform", width=130)
tabelle.column("status", width=120)
tabelle.column("note", width=80)

for modul in module:
    tabelle.insert("", "end", values=modul)

tabelle.pack(fill="both", expand=True)

fenster.mainloop()
