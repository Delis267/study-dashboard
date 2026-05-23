import tkinter as tk
from tkinter import messagebox
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
STATUS_WERTE = ("anerkannt", "fertig", "in Arbeit", "offen")

dashboard_anzeigen = {}
formular_felder = {}
aktiver_editor = None
kontextmenue = None


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


def aktualisiere_modulliste_aus_tabelle():
    module.clear()

    for zeile in tabelle.get_children():
        werte = list(tabelle.item(zeile, "values"))[:6]
        werte[1] = int(werte[1])
        module.append(tuple(werte))


def aktualisiere_dashboard():
    kennzahlen = berechne_kennzahlen()

    dashboard_anzeigen["ects"].config(text=f"{kennzahlen['abgeschlossen']}/{ZIEL_ECTS}")
    dashboard_anzeigen["ects_prozent"].config(text=f"{kennzahlen['prozent_fertig']}% fertig")

    status_werte = [
        ("anerkannt", kennzahlen["anerkannt"], FARBEN["anerkannt"]),
        ("fertig", kennzahlen["fertig"], FARBEN["fertig"]),
        ("in Arbeit", kennzahlen["in Arbeit"], FARBEN["in Arbeit"]),
        ("offen", kennzahlen["offen"], FARBEN["offen"]),
    ]

    zeichne_donut(dashboard_anzeigen["donut"], status_werte)

    for name, ects, farbe in status_werte:
        dashboard_anzeigen["legende"][name].config(text=f"{ects} ECTS {name}")


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
    dashboard_anzeigen["donut"] = donut
    zeichne_donut(donut, status_werte)

    legende = tk.Frame(diagramm_bereich, bg=FARBEN["hintergrund"])
    legende.grid(row=0, column=1, sticky="w")
    dashboard_anzeigen["legende"] = {}

    for zeile, status_wert in enumerate(status_werte):
        name, ects, farbe = status_wert
        farbfeld = tk.Label(legende, text="  ", bg=farbe, highlightthickness=1, highlightbackground=FARBEN["rahmen"])
        farbfeld.grid(row=zeile, column=0, padx=(0, 8), pady=4)
        legenden_text = tk.Label(legende, text=f"{ects} ECTS {name}", bg=FARBEN["hintergrund"], font=("Segoe UI", 10))
        legenden_text.grid(row=zeile, column=1, sticky="w")
        dashboard_anzeigen["legende"][name] = legenden_text

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

    for index, zeile in enumerate(zeilen):
        text, schrift = zeile
        wert_label = tk.Label(inhalt, text=text, bg=farbe, anchor="w", justify="left", font=schrift)
        wert_label.pack(anchor="w")

        if titel == "ECTS" and index == 0:
            dashboard_anzeigen["ects"] = wert_label
        if titel == "ECTS" and index == 1:
            dashboard_anzeigen["ects_prozent"] = wert_label


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


def leere_hinzufuegen_formular():
    for feldname in formular_felder:
        formular_felder[feldname].set("")

    formular_felder["ects"].set("5")
    formular_felder["status"].set("offen")


def lese_formularwerte():
    kuerzel = formular_felder["kuerzel"].get().strip()
    ects_text = formular_felder["ects"].get().strip()
    kursname = formular_felder["kursname"].get().strip()
    pruefungsform = formular_felder["pruefungsform"].get().strip()
    status = formular_felder["status"].get().strip()
    note = formular_felder["note"].get().strip()

    if kuerzel == "" or kursname == "":
        messagebox.showwarning("Eingabe fehlt", "Bitte mindestens Kuerzel und Kursname eintragen.")
        return None

    try:
        ects = int(ects_text)
    except ValueError:
        messagebox.showwarning("ECTS ungueltig", "ECTS muss eine ganze Zahl sein.")
        return None

    if ects <= 0:
        messagebox.showwarning("ECTS ungueltig", "ECTS muss groesser als 0 sein.")
        return None

    if status not in STATUS_WERTE:
        messagebox.showwarning("Status ungueltig", "Bitte einen gueltigen Status auswaehlen.")
        return None

    return (kuerzel, ects, kursname, pruefungsform, status, note)


def modul_hinzufuegen():
    werte = lese_formularwerte()

    if werte is None:
        return

    neue_zeile = tabelle.insert("", "end", values=werte)
    tabelle.selection_set(neue_zeile)
    tabelle.see(neue_zeile)
    leere_hinzufuegen_formular()
    aktualisiere_modulliste_aus_tabelle()
    aktualisiere_dashboard()


def module_loeschen(zeilen):
    if not zeilen:
        return

    for zeile in zeilen:
        tabelle.delete(zeile)

    aktualisiere_modulliste_aus_tabelle()
    aktualisiere_dashboard()


def ausgewaehlte_module_loeschen(event=None):
    module_loeschen(tabelle.selection())


def starte_zelleneditor(event):
    global aktiver_editor

    zeile = tabelle.identify_row(event.y)
    spalte_id = tabelle.identify_column(event.x)

    if zeile == "" or spalte_id == "":
        return

    spalten = ("kuerzel", "ects", "kursname", "pruefungsform", "status", "note")
    spalten_index = int(spalte_id.replace("#", "")) - 1
    spalte = spalten[spalten_index]

    if spalte not in ("kuerzel", "ects", "kursname", "pruefungsform", "status", "note"):
        return

    if aktiver_editor is not None:
        aktiver_editor.destroy()
        aktiver_editor = None

    x, y, breite, hoehe = tabelle.bbox(zeile, spalte_id)
    werte = list(tabelle.item(zeile, "values"))
    alter_wert = werte[spalten_index]

    variable = tk.StringVar(value=alter_wert)

    if spalte == "status":
        editor = ttk.Combobox(tabelle, textvariable=variable, values=STATUS_WERTE, state="readonly")
    else:
        editor = ttk.Entry(tabelle, textvariable=variable)

    editor.place(x=x, y=y, width=breite, height=hoehe)
    editor.focus_set()
    aktiver_editor = editor

    def speichern(event=None):
        global aktiver_editor

        neuer_wert = variable.get().strip()

        if spalte == "ects":
            try:
                neuer_wert = int(neuer_wert)
            except ValueError:
                messagebox.showwarning("ECTS ungueltig", "ECTS muss eine ganze Zahl sein.")
                editor.focus_set()
                return

            if neuer_wert <= 0:
                messagebox.showwarning("ECTS ungueltig", "ECTS muss groesser als 0 sein.")
                editor.focus_set()
                return

        if spalte == "status" and neuer_wert not in STATUS_WERTE:
            return

        werte[spalten_index] = neuer_wert
        tabelle.item(zeile, values=werte)
        editor.destroy()
        aktiver_editor = None
        aktualisiere_modulliste_aus_tabelle()
        aktualisiere_dashboard()

    def abbrechen(event=None):
        global aktiver_editor

        editor.destroy()
        aktiver_editor = None

    editor.bind("<Return>", speichern)
    editor.bind("<FocusOut>", speichern)
    editor.bind("<Escape>", abbrechen)

    if spalte == "status":
        editor.bind("<<ComboboxSelected>>", speichern)


def zeige_kontextmenue(event):
    zeile = tabelle.identify_row(event.y)

    if zeile == "":
        return

    if zeile not in tabelle.selection():
        tabelle.selection_set(zeile)

    kontextmenue.tk_popup(event.x_root, event.y_root)


def erstelle_kontextmenue(parent):
    global kontextmenue

    kontextmenue = tk.Menu(parent, tearoff=False)
    kontextmenue.add_command(label="Ausgewaehlte Module loeschen", command=ausgewaehlte_module_loeschen)


def erstelle_hinzufuegen_formular(parent):
    detail = tk.Frame(parent, bg=FARBEN["hintergrund"], highlightthickness=2, highlightbackground=FARBEN["rahmen"], padx=12, pady=10)
    detail.grid(row=1, column=0, sticky="ew", pady=(12, 0))

    tk.Label(detail, text="Neues Modul", bg=FARBEN["hintergrund"], font=("Segoe UI", 13, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 12))

    feld_definitionen = [
        ("kuerzel", "Kuerzel", 13, 0),
        ("ects", "ECTS", 6, 0),
        ("kursname", "Kursname", 28, 1),
        ("pruefungsform", "Pruefungsform", 16, 0),
        ("status", "Status", 13, 0),
        ("note", "Note", 8, 0),
    ]

    for spalte, feld in enumerate(feld_definitionen, start=1):
        feldname, beschriftung, breite, gewicht = feld
        feldrahmen = tk.Frame(detail, bg=FARBEN["hintergrund"])
        feldrahmen.grid(row=0, column=spalte, sticky="ew", padx=(0, 8))

        tk.Label(feldrahmen, text=beschriftung, bg=FARBEN["hintergrund"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        variable = tk.StringVar()
        formular_felder[feldname] = variable

        if feldname == "status":
            eingabe = ttk.Combobox(feldrahmen, textvariable=variable, values=STATUS_WERTE, width=breite, state="readonly")
        else:
            eingabe = ttk.Entry(feldrahmen, textvariable=variable, width=breite)

        eingabe.pack(fill="x")
        detail.columnconfigure(spalte, weight=gewicht)

    button_bereich = tk.Frame(detail, bg=FARBEN["hintergrund"])
    button_bereich.grid(row=0, column=7, sticky="sew")

    ttk.Button(button_bereich, text="Hinzufuegen", command=modul_hinzufuegen).grid(row=0, column=0, sticky="ew", pady=(17, 0), padx=(0, 6))
    ttk.Button(button_bereich, text="Leeren", command=leere_hinzufuegen_formular).grid(row=0, column=1, sticky="ew", pady=(17, 0))

    leere_hinzufuegen_formular()


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

    tabelleninhalt = tk.Frame(tabellen_bereich, bg=FARBEN["hintergrund"])
    tabelleninhalt.pack(fill="both", expand=True)

    listenbereich = tk.Frame(tabelleninhalt, bg=FARBEN["hintergrund"])
    listenbereich.grid(row=0, column=0, sticky="nsew")

    erstelle_hinzufuegen_formular(tabelleninhalt)

    tabelle = ttk.Treeview(
        listenbereich,
        columns=("kuerzel", "ects", "kursname", "pruefungsform", "status", "note"),
        show="headings",
        height=14,
        selectmode="extended",
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

    scrollbar = ttk.Scrollbar(listenbereich, orient="vertical", command=tabelle.yview)
    tabelle.configure(yscrollcommand=scrollbar.set)
    tabelle.bind("<Double-1>", starte_zelleneditor)
    tabelle.bind("<Delete>", ausgewaehlte_module_loeschen)
    tabelle.bind("<Button-3>", zeige_kontextmenue)
    tabelle.bind("<Button-2>", zeige_kontextmenue)
    erstelle_kontextmenue(tabelle)

    tabelle.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    listenbereich.rowconfigure(0, weight=1)
    listenbereich.columnconfigure(0, weight=1)
    tabelleninhalt.rowconfigure(0, weight=1)
    tabelleninhalt.columnconfigure(0, weight=1)


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
