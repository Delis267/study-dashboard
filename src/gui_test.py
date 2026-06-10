import tkinter as tk
from tkinter import ttk


# Einfacher Machbarkeitstest:
# Kann Tkinter ein Donutdiagramm und eine Modultabelle darstellen?

module = [
    ("IGIS01", 5, "Grundlagen der Softwaretechnik", "Klausur", "anerkannt", ""),
    ("IREN01", 5, "Requirements Engineering", "Klausur", "fertig", "1.7"),
    ("ISPE01", 5, "Spezifikation", "Klausur", "fertig", "1.3"),
    ("IPWA01", 5, "Web-Anwendungsoberflaechen", "Projekt", "fertig", "1.7"),
    ("DLBCSEMSE01", 5, "Mobile Software Engineering I", "Projekt", "in Arbeit", ""),
    ("ISSE01", 5, "Seminar Software Engineering", "Seminar", "offen", ""),
    ("IWNFE02", 5, "Projekt Agiles Software Engineering", "Projekt", "offen", ""),
]

farben = {
    "anerkannt": "#7ee08b",
    "fertig": "#34c969",
    "in Arbeit": "#ffe680",
    "offen": "#a9d8f5",
}


def berechne_ects(status):
    summe = 0

    for modul in module:
        if modul[4] == status:
            summe = summe + modul[1]

    return summe


def zeichne_donut(canvas):
    werte = [
        ("anerkannt", berechne_ects("anerkannt")),
        ("fertig", berechne_ects("fertig")),
        ("in Arbeit", berechne_ects("in Arbeit")),
        ("offen", berechne_ects("offen")),
    ]

    gesamt = sum(wert for status, wert in werte)
    start_winkel = 90

    for status, wert in werte:
        winkel = 360 * wert / gesamt
        canvas.create_arc(10, 10, 190, 190, start=start_winkel, extent=winkel, fill=farben[status], outline="white")
        start_winkel = start_winkel + winkel

    canvas.create_oval(70, 70, 130, 130, fill="white", outline="black")


def erstelle_legende(parent):
    for zeile, status in enumerate(farben):
        tk.Label(parent, text="  ", bg=farben[status], relief="solid").grid(row=zeile, column=0, padx=5, pady=3)
        tk.Label(parent, text=f"{berechne_ects(status)} ECTS {status}").grid(row=zeile, column=1, sticky="w")


def erstelle_tabelle(parent):
    spalten = ("kuerzel", "ects", "kursname", "pruefungsform", "status", "note")
    tabelle = ttk.Treeview(parent, columns=spalten, show="headings")

    for spalte in spalten:
        tabelle.heading(spalte, text=spalte)

    tabelle.column("kuerzel", width=120)
    tabelle.column("ects", width=50)
    tabelle.column("kursname", width=280)
    tabelle.column("pruefungsform", width=120)
    tabelle.column("status", width=100)
    tabelle.column("note", width=60)

    for modul in module:
        tabelle.insert("", "end", values=modul)

    tabelle.pack(fill="both", expand=True)


fenster = tk.Tk()
fenster.title("GUI-Machbarkeitstest")
fenster.geometry("820x520")

kopfbereich = tk.Frame(fenster, padx=15, pady=15)
kopfbereich.pack(fill="x")

donut = tk.Canvas(kopfbereich, width=200, height=200)
donut.pack(side="left")
zeichne_donut(donut)

legende = tk.Frame(kopfbereich, padx=20)
legende.pack(side="left")
erstelle_legende(legende)

tabellenbereich = tk.Frame(fenster, padx=15, pady=15)
tabellenbereich.pack(fill="both", expand=True)
erstelle_tabelle(tabellenbereich)

fenster.mainloop()
