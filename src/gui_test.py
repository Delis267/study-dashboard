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


FARBEN = {
    "anerkannt": "#7ee08b",
    "fertig": "#34c969",
    "in Arbeit": "#ffe680",
    "offen": "#a9d8f5",
    "prognose": "#ffc3c7",
    "rahmen": "#222222",
    "hintergrund": "#fbfbf8",
}

ZIEL_ECTS = 180
ZIEL_NOTENSCHNITT = "2.0"
AKTUELLER_NOTENSCHNITT = "1.7"
ZIEL_VELOCITY = 5
AKTUELLE_VELOCITY = 6
PROGNOSE_ENDE = "01.06.2027"


def berechne_ects(status):
    summe = 0

    for modul in module:
        if modul[4] == status:
            summe = summe + modul[1]

    return summe


def berechne_kennzahlen():
    ects_anerkannt = berechne_ects("anerkannt")
    ects_fertig = berechne_ects("fertig")
    ects_in_arbeit = berechne_ects("in Arbeit")
    ects_offen = berechne_ects("offen")
    ects_abgeschlossen = ects_anerkannt + ects_fertig
    prozent_fertig = round(ects_abgeschlossen / ZIEL_ECTS * 100)

    return {
        "anerkannt": ects_anerkannt,
        "fertig": ects_fertig,
        "in Arbeit": ects_in_arbeit,
        "offen": ects_offen,
        "abgeschlossen": ects_abgeschlossen,
        "prozent_fertig": prozent_fertig,
    }


def zeichne_donut(canvas, werte):
    gesamt = sum(wert[1] for wert in werte)
    start_winkel = 120

    canvas.delete("all")

    for name, ects, farbe in werte:
        if gesamt == 0:
            continue

        winkel = 360 * ects / gesamt
        canvas.create_arc(
            8,
            8,
            148,
            148,
            start=start_winkel,
            extent=winkel,
            fill=farbe,
            outline=FARBEN["rahmen"],
            width=2,
        )
        start_winkel = start_winkel + winkel

    canvas.create_oval(54, 54, 102, 102, fill=FARBEN["hintergrund"], outline=FARBEN["rahmen"], width=2)


def erstelle_kopfbereich(parent, kennzahlen):
    kopfbereich = tk.Frame(parent, bg=FARBEN["hintergrund"], highlightthickness=2, highlightbackground=FARBEN["rahmen"])
    kopfbereich.pack(fill="x")

    info_bereich = tk.Frame(kopfbereich, bg=FARBEN["hintergrund"], padx=14, pady=10)
    info_bereich.grid(row=0, column=0, sticky="nsew")

    tk.Label(info_bereich, text="Study-Dashboard", bg=FARBEN["hintergrund"], font=("Segoe UI", 23, "bold")).pack(anchor="w")

    infos = [
        "B. Sc. Softwareentwicklung",
        "Studienstart: 01.03.2024",
        "Regelstudienzeit: 01.03.2027",
        "Ziel-ECTS: 180",
    ]

    for text in infos:
        tk.Label(info_bereich, text="<> " + text, bg=FARBEN["hintergrund"], font=("Segoe UI", 11)).pack(anchor="w")

    diagramm_bereich = tk.Frame(kopfbereich, bg=FARBEN["hintergrund"], padx=18, pady=8)
    diagramm_bereich.grid(row=0, column=1, sticky="e")

    status_werte = [
        ("anerkannt", kennzahlen["anerkannt"], FARBEN["anerkannt"]),
        ("fertig", kennzahlen["fertig"], FARBEN["fertig"]),
        ("in Arbeit", kennzahlen["in Arbeit"], FARBEN["in Arbeit"]),
        ("offen", kennzahlen["offen"], FARBEN["offen"]),
    ]

    donut = tk.Canvas(diagramm_bereich, width=156, height=156, bg=FARBEN["hintergrund"], highlightthickness=0)
    donut.grid(row=0, column=0, padx=(0, 20))
    zeichne_donut(donut, status_werte)

    legende = tk.Frame(diagramm_bereich, bg=FARBEN["hintergrund"])
    legende.grid(row=0, column=1, sticky="w")

    for zeile, status_wert in enumerate(status_werte):
        name, ects, farbe = status_wert
        farbfeld = tk.Label(legende, text="  ", bg=farbe, highlightthickness=1, highlightbackground=FARBEN["rahmen"])
        farbfeld.grid(row=zeile, column=0, padx=(0, 8), pady=4)
        tk.Label(legende, text=f"{ects} ECTS {name}", bg=FARBEN["hintergrund"], font=("Segoe UI", 10)).grid(row=zeile, column=1, sticky="w")

    kopfbereich.columnconfigure(0, weight=1)


def erstelle_kennzahl(parent, spalte, titel, zeilen, farbe):
    kachel = tk.Frame(parent, bg=farbe, highlightthickness=2, highlightbackground=FARBEN["rahmen"])
    kachel.grid(row=0, column=spalte, sticky="nsew", padx=12)

    titel_label = tk.Label(
        kachel,
        text=titel,
        bg=farbe,
        anchor="w",
        padx=9,
        pady=3,
        font=("Segoe UI", 11, "bold"),
        highlightthickness=1,
        highlightbackground=FARBEN["rahmen"],
    )
    titel_label.pack(fill="x")

    inhalt = tk.Frame(kachel, bg=farbe, padx=10, pady=10)
    inhalt.pack(fill="both", expand=True)

    for text, schrift in zeilen:
        tk.Label(inhalt, text=text, bg=farbe, anchor="w", justify="left", font=schrift).pack(anchor="w")


def erstelle_kennzahlenbereich(parent, kennzahlen):
    kachel_bereich = tk.Frame(parent, bg=FARBEN["hintergrund"], pady=16)
    kachel_bereich.pack(fill="x")

    erstelle_kennzahl(
        kachel_bereich,
        0,
        "ECTS",
        [
            (f"{kennzahlen['abgeschlossen']}/{ZIEL_ECTS}", ("Segoe UI", 13)),
            (f"{kennzahlen['prozent_fertig']}% fertig", ("Segoe UI", 13, "bold")),
        ],
        "#b5f1bd",
    )
    erstelle_kennzahl(
        kachel_bereich,
        1,
        "Notenschnitt",
        [
            (f"Ziel: {ZIEL_NOTENSCHNITT}", ("Segoe UI", 11)),
            (f"Aktuell: {AKTUELLER_NOTENSCHNITT}", ("Segoe UI", 13, "bold")),
        ],
        FARBEN["offen"],
    )
    erstelle_kennzahl(
        kachel_bereich,
        2,
        "Velocity",
        [
            (f"Ziel: {ZIEL_VELOCITY} ECTS/Monat", ("Segoe UI", 11)),
            (f"Aktuell: {AKTUELLE_VELOCITY} ECTS/Monat", ("Segoe UI", 12, "bold")),
        ],
        FARBEN["in Arbeit"],
    )
    erstelle_kennzahl(
        kachel_bereich,
        3,
        "Prognose",
        [
            (f"Ende: {PROGNOSE_ENDE}", ("Segoe UI", 11, "bold")),
            ("3 Monate", ("Segoe UI", 11)),
            ("hinter Plan", ("Segoe UI", 11)),
        ],
        FARBEN["prognose"],
    )

    for spalte in range(4):
        kachel_bereich.columnconfigure(spalte, weight=1, uniform="kennzahlen")


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


def erstelle_tabelle(parent):
    global tabelle
    global sortierung_absteigend

    trennlinie = tk.Frame(parent, height=3, bg=FARBEN["rahmen"])
    trennlinie.pack(fill="x", pady=(2, 14))

    tabellen_bereich = tk.Frame(parent, bg=FARBEN["hintergrund"], highlightthickness=2, highlightbackground=FARBEN["rahmen"], padx=14, pady=14)
    tabellen_bereich.pack(fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=27, background="white", fieldbackground="white")
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=6)

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
        height=14,
    )

    tabelle.heading("kuerzel", text="Kuerzel", command=lambda: sortiere_tabelle("kuerzel"))
    tabelle.heading("ects", text="ECTS", command=lambda: sortiere_tabelle("ects"))
    tabelle.heading("kursname", text="Kursname", command=lambda: sortiere_tabelle("kursname"))
    tabelle.heading("pruefungsform", text="Pruefungsform", command=lambda: sortiere_tabelle("pruefungsform"))
    tabelle.heading("status", text="Status", command=lambda: sortiere_tabelle("status"))
    tabelle.heading("note", text="Note", command=lambda: sortiere_tabelle("note"))

    tabelle.column("kuerzel", width=140, anchor="w", stretch=False)
    tabelle.column("ects", width=70, anchor="center", stretch=False)
    tabelle.column("kursname", width=420, anchor="w", stretch=True)
    tabelle.column("pruefungsform", width=145, anchor="w", stretch=False)
    tabelle.column("status", width=140, anchor="w", stretch=False)
    tabelle.column("note", width=80, anchor="center", stretch=False)

    for modul in module:
        tabelle.insert("", "end", values=modul)

    scrollbar = ttk.Scrollbar(tabellen_bereich, orient="vertical", command=tabelle.yview)
    tabelle.configure(yscrollcommand=scrollbar.set)

    tabelle.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    tabellen_bereich.rowconfigure(0, weight=1)
    tabellen_bereich.columnconfigure(0, weight=1)


fenster = tk.Tk()
fenster.title("Study-Dashboard")
fenster.geometry("980x760")
fenster.minsize(880, 640)
fenster.configure(bg=FARBEN["hintergrund"])

hauptbereich = tk.Frame(fenster, bg=FARBEN["hintergrund"], padx=8, pady=8)
hauptbereich.pack(fill="both", expand=True)

kennzahlen = berechne_kennzahlen()
erstelle_kopfbereich(hauptbereich, kennzahlen)
erstelle_kennzahlenbereich(hauptbereich, kennzahlen)
erstelle_tabelle(hauptbereich)

fenster.mainloop()
