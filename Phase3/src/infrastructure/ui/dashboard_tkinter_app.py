import tkinter as tk
from tkinter import messagebox, ttk

from application.dtos.dashboard_daten import DashboardDaten, ModulDaten
from application.ports.studien_analyse_input_port import StudienAnalyseInputPort
from application.ports.studium_bearbeiten_input_port import StudiumBearbeitenInputPort
from domain.modul_status import ModulStatus
from domain.pruefungsform import Pruefungsform
from domain.pruefungsversuch import ERLAUBTE_NOTEN


def popup_am_cursor_platzieren(
    dialog: tk.Toplevel,
    parent: tk.Tk,
    breite: int = 640,
) -> None:
    dialog.update_idletasks()
    hoehe = dialog.winfo_reqheight()
    x = parent.winfo_pointerx()
    y = parent.winfo_pointery()
    max_x = max(dialog.winfo_screenwidth() - breite - 12, 0)
    max_y = max(dialog.winfo_screenheight() - hoehe - 48, 0)
    x = min(max(x, 12), max_x)
    y = min(max(y, 12), max_y)
    dialog.minsize(breite, hoehe)
    dialog.geometry(f"{breite}x{hoehe}+{x}+{y}")


class DashboardTkinterApp:
    KENNZAHL_BOX_HOEHE = 104

    def __init__(
        self,
        analyse_port: StudienAnalyseInputPort,
        bearbeiten_port: StudiumBearbeitenInputPort,
    ) -> None:
        self.analyse_port = analyse_port
        self.bearbeiten_port = bearbeiten_port
        self.fenster = tk.Tk()
        self.fenster.title("Studien-Dashboard")
        self.fenster.geometry("1120x720")
        self._module: dict[str, ModulDaten] = {}

        self._oberflaeche_erstellen()
        self.aktualisieren()

    def starten(self) -> None:
        self.fenster.mainloop()

    def _oberflaeche_erstellen(self) -> None:
        hauptbereich = ttk.Frame(self.fenster, padding=12)
        hauptbereich.pack(fill="both", expand=True)

        kopfbereich = tk.Frame(
            hauptbereich,
            background="white",
            borderwidth=1,
            relief="solid",
        )
        kopfbereich.pack(fill="x")
        kopfbereich.columnconfigure(0, weight=1)

        kopf_oben = tk.Frame(kopfbereich, background="white", padx=16, pady=12)
        kopf_oben.grid(row=0, column=0, sticky="ew")
        kopf_oben.columnconfigure(0, weight=1)

        info_frame = tk.Frame(kopf_oben, background="white")
        info_frame.grid(row=0, column=0, sticky="nsew")
        tk.Label(
            info_frame,
            text="Study-Dashboard",
            background="white",
            font=("TkDefaultFont", 18, "bold"),
        ).pack(anchor="w", pady=(0, 6))

        self.studieninfo_labels: dict[str, tk.Label] = {}
        for titel in ("Studiengang", "Studienstart", "Regelstudienzeit", "Ziel-ECTS"):
            label = tk.Label(
                info_frame,
                text="",
                background="white",
                anchor="w",
                font=("TkDefaultFont", 10),
            )
            label.pack(anchor="w")
            self.studieninfo_labels[titel] = label

        self.donut_canvas = tk.Canvas(
            kopf_oben,
            width=150,
            height=150,
            background="white",
            highlightthickness=0,
        )
        self.donut_canvas.grid(row=0, column=1, padx=24)

        self.legende_canvas = tk.Canvas(
            kopf_oben,
            width=210,
            height=130,
            background="white",
            highlightthickness=0,
        )
        self.legende_canvas.grid(row=0, column=2, sticky="e")

        tk.Frame(kopfbereich, height=1, background="#222222").grid(
            row=1,
            column=0,
            sticky="ew",
        )

        self.kennzahl_boxen: dict[str, dict[str, tk.Label]] = {}
        boxen_frame = tk.Frame(kopfbereich, background="white", padx=16, pady=10)
        boxen_frame.grid(row=2, column=0, sticky="ew")
        for spalte in range(4):
            boxen_frame.columnconfigure(spalte, weight=1, uniform="kennzahlen")

        self._kennzahl_box_erstellen(boxen_frame, "ECTS", "#b6efbf", 0)
        self._kennzahl_box_erstellen(boxen_frame, "Notenschnitt", "#a9d8f4", 1)
        self._kennzahl_box_erstellen(boxen_frame, "Velocity", "#ffe89a", 2)
        self._kennzahl_box_erstellen(boxen_frame, "Prognose", "#ffc6c8", 3)

        aktionen = ttk.Frame(hauptbereich)
        aktionen.pack(fill="x", pady=(10, 0))
        ttk.Button(
            aktionen,
            text="Neues Modul hinzufügen",
            command=self.modul_hinzufuegen,
        ).pack(side="left")

        tabellenbereich = ttk.Frame(hauptbereich)
        tabellenbereich.pack(fill="both", expand=True, pady=(12, 0))
        self._tabelle_erstellen(tabellenbereich)


    def _kennzahl_box_erstellen(
        self,
        parent: tk.Frame,
        titel: str,
        farbe: str,
        spalte: int,
    ) -> None:
        box = tk.Frame(
            parent,
            background=farbe,
            borderwidth=1,
            height=self.KENNZAHL_BOX_HOEHE,
            relief="solid",
            padx=10,
            pady=8,
        )
        box.grid(row=0, column=spalte, sticky="ew", padx=(0 if spalte == 0 else 8, 0))
        box.pack_propagate(False)

        tk.Label(
            box,
            text=titel,
            background=farbe,
            anchor="w",
            font=("TkDefaultFont", 10, "bold"),
        ).pack(fill="x")
        primaer_label = tk.Label(
            box,
            text="",
            background=farbe,
            anchor="w",
            font=("TkDefaultFont", 12, "bold"),
        )
        primaer_label.pack(fill="x", pady=(6, 0))
        sekundaer_label = tk.Label(
            box,
            text="",
            background=farbe,
            anchor="w",
            justify="left",
        )
        sekundaer_label.pack(fill="x", pady=(2, 0))
        self.kennzahl_boxen[titel] = {
            "primaer": primaer_label,
            "sekundaer": sekundaer_label,
        }

    def _tabelle_erstellen(self, parent: ttk.Frame) -> None:
        spalten = (
            "kurs_id",
            "ects",
            "kursname",
            "pruefungsform",
            "status",
            "note"
        )
        self.tabelle = ttk.Treeview(parent, columns=spalten, show="headings", height=18)

        ueberschriften = {
            "kurs_id": "Kurs-ID",
            "ects": "ECTS",
            "kursname": "Kursname",
            "status": "Status",
            "pruefungsform": "Pruefungsform",
            "note": "Note",
        }
        breiten = {
            "kurs_id": 100,
            "ects": 55,
            "kursname": 330,
            "status": 110,
            "pruefungsform": 130,
            "note": 80,
        }

        for spalte in spalten:
            self.tabelle.heading(spalte, text=ueberschriften[spalte])
            self.tabelle.column(spalte, width=breiten[spalte], anchor="w")

        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tabelle.yview)
        self.tabelle.configure(yscrollcommand=scrollbar.set)
        self.tabelle.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tabelle.bind("<Double-1>", self._tabellendoppelklick)

    def aktualisieren(self) -> None:
        dashboard_daten = self.analyse_port.dashboard_daten_abrufen()
        self._kennzahlen_aktualisieren(dashboard_daten)
        self._donut_zeichnen(dashboard_daten)
        self._tabelle_aktualisieren(dashboard_daten.module)

    def modul_hinzufuegen(self) -> None:
        dialog = ModulHinzufuegenDialog(self.fenster)
        modul = dialog.anzeigen()
        if modul is None:
            return

        try:
            self.bearbeiten_port.modul_hinzufuegen(
                kurs_id=modul["kurs_id"],
                kursname=modul["kursname"],
                ects=modul["ects"],
                pruefungsform=modul["pruefungsform"],
                ist_anerkannt=modul["ist_anerkannt"],
            )
            if modul["note"] is not None:
                self.bearbeiten_port.modul_bearbeiten(
                    kurs_id=modul["kurs_id"],
                    kursname=modul["kursname"],
                    ects=modul["ects"],
                    pruefungsform=modul["pruefungsform"],
                    note=modul["note"],
                )
            self.aktualisieren()
        except ValueError as fehler:
            messagebox.showerror("Modul nicht angelegt", str(fehler))

    def modul_loeschen(self, modul: ModulDaten) -> None:
        if not messagebox.askyesno("Modul loeschen", f"Modul {modul.kurs_id} loeschen?"):
            return

        try:
            self.bearbeiten_port.modul_loeschen(modul.kurs_id)
            self.aktualisieren()
        except ValueError as fehler:
            messagebox.showerror("Loeschen nicht moeglich", str(fehler))

    def modul_bearbeiten(self, modul: ModulDaten) -> None:
        dialog = ModulBearbeitenDialog(self.fenster, modul)
        aktion = dialog.anzeigen()
        if aktion is None:
            return

        try:
            if aktion["typ"] == "loeschen":
                self.modul_loeschen(modul)
                return
            self.bearbeiten_port.modul_bearbeiten(
                kurs_id=modul.kurs_id,
                kursname=aktion["kursname"],
                ects=aktion["ects"],
                pruefungsform=aktion["pruefungsform"],
                note=aktion["note"],
            )
            self.aktualisieren()
        except ValueError as fehler:
            messagebox.showerror("Modul nicht gespeichert", str(fehler))

    def _tabellendoppelklick(self, event: tk.Event) -> None:
        zeile = self.tabelle.identify_row(event.y)
        if not zeile:
            return

        modul = self._module[str(zeile)]
        self.modul_bearbeiten(modul)

    def _kennzahlen_aktualisieren(self, daten: DashboardDaten) -> None:
        self.studieninfo_labels["Studiengang"].configure(
            text=f"o {daten.studiengang}"
        )
        self.studieninfo_labels["Studienstart"].configure(
            text=f"o Studienstart: {daten.startdatum}"
        )
        self.studieninfo_labels["Regelstudienzeit"].configure(
            text=f"o Regelstudienzeit: bis {daten.zieldatum}"
        )
        self.studieninfo_labels["Ziel-ECTS"].configure(
            text=f"o Ziel-ECTS: {daten.gesamt_ects}"
        )

        self.kennzahl_boxen["ECTS"]["primaer"].configure(
            text=f"{daten.erreichte_ects}/{daten.gesamt_ects}"
        )
        self.kennzahl_boxen["ECTS"]["sekundaer"].configure(
            text=f"{daten.fortschritt_prozent} % fertig\n{daten.offene_ects} ECTS offen"
        )

        notenschnitt = "-" if daten.notendurchschnitt is None else daten.notendurchschnitt
        ziel_erreicht = self._zieltext(daten.ziel_notendurchschnitt_erreicht)
        self.kennzahl_boxen["Notenschnitt"]["primaer"].configure(
            text=f"Aktuell: {notenschnitt}"
        )
        self.kennzahl_boxen["Notenschnitt"]["sekundaer"].configure(
            text=f"Ziel: {daten.ziel_notendurchschnitt}\n{ziel_erreicht}"
        )
        self.kennzahl_boxen["Velocity"]["primaer"].configure(
            text=f"{daten.velocity_ects_pro_monat} ECTS/Monat"
        )
        prognose = "-" if daten.prognostiziertes_ende is None else daten.prognostiziertes_ende
        self.kennzahl_boxen["Velocity"]["sekundaer"].configure(
            text=f"Ziel: {daten.ziel_velocity_ects_pro_monat} ECTS/Monat\n{self._velocity_hinweis(daten)}"
        )

        self.kennzahl_boxen["Prognose"]["primaer"].configure(text=f"Ende: {prognose}")
        self.kennzahl_boxen["Prognose"]["sekundaer"].configure(
            text=self._prognose_hinweis(daten)
        )
        self._legende_zeichnen(daten)

    def _donut_zeichnen(self, daten: DashboardDaten) -> None:
        self.donut_canvas.delete("all")
        farben = self._status_farben()
        werte = [
            (status, daten.ects_nach_status.get(status, 0))
            for status in (
                ModulStatus.ANERKANNT,
                ModulStatus.FERTIG,
                ModulStatus.IN_ARBEIT,
                ModulStatus.OFFEN,
            )
        ]
        gesamt = sum(wert for _status, wert in werte)
        if gesamt == 0:
            self.donut_canvas.create_text(90, 90, text="0 ECTS")
            return

        start_winkel = 90
        for status, wert in werte:
            if wert == 0:
                continue
            winkel = 360 * wert / gesamt
            self.donut_canvas.create_arc(
                8,
                8,
                142,
                142,
                start=start_winkel,
                extent=winkel,
                fill=farben[status],
                outline="white",
            )
            start_winkel += winkel

        self.donut_canvas.create_oval(53, 53, 97, 97, fill="white", outline="white")
        self.donut_canvas.create_text(75, 75, text=f"{daten.erreichte_ects}\nECTS")

    def _legende_zeichnen(self, daten: DashboardDaten) -> None:
        self.legende_canvas.delete("all")
        farben = self._status_farben()
        eintraege = (
            (ModulStatus.ANERKANNT, "anerkannt"),
            (ModulStatus.FERTIG, "fertig"),
            (ModulStatus.IN_ARBEIT, "in Arbeit"),
            (ModulStatus.OFFEN, "offen"),
        )
        for index, (status, beschriftung) in enumerate(eintraege):
            y = 14 + index * 28
            ects = daten.ects_nach_status.get(status, 0)
            self.legende_canvas.create_rectangle(
                4,
                y,
                18,
                y + 14,
                fill=farben[status],
                outline="#333333",
            )
            self.legende_canvas.create_text(
                28,
                y + 7,
                text=f"{ects} ECTS {beschriftung}",
                anchor="w",
            )

    def _tabelle_aktualisieren(self, module: list[ModulDaten]) -> None:
        self._module = {modul.kurs_id: modul for modul in module}
        for eintrag in self.tabelle.get_children():
            self.tabelle.delete(eintrag)

        for modul in module:
            self.tabelle.insert(
                "",
                "end",
                iid=modul.kurs_id,
                values=(
                    modul.kurs_id,
                    modul.ects,
                    modul.kursname,
                    "-" if modul.pruefungsform is None else modul.pruefungsform,
                    modul.status.value,
                    "-" if modul.note is None else modul.note,
                    "Doppelklick",
                ),
            )

    def _zieltext(self, ziel_erreicht: bool | None) -> str:
        if ziel_erreicht is None:
            return "noch keine Note"
        if ziel_erreicht:
            return "erreicht"
        return "nicht erreicht"

    def _velocity_hinweis(self, daten: DashboardDaten) -> str:
        if daten.ziel_velocity_ects_pro_monat <= daten.velocity_ects_pro_monat:
            return "erreicht"
        if daten.ziel_velocity_ects_pro_monat >= daten.ziel_velocity_ects_pro_monat:
            return "nicht erreicht"

    def _prognose_hinweis(self, daten: DashboardDaten) -> str:
        if daten.prognostiziertes_ende is None:
            return "Noch keine Prognose"
        if daten.prognostiziertes_ende <= daten.zieldatum:
            return "im Plan"
        return "hinter Plan"

    def _status_farben(self) -> dict[ModulStatus, str]:
        return {
            ModulStatus.ANERKANNT: "#66d56f",
            ModulStatus.FERTIG: "#37b56d",
            ModulStatus.IN_ARBEIT: "#ffd768",
            ModulStatus.OFFEN: "#9fc8ee",
        }


class ModulHinzufuegenDialog:
    def __init__(self, parent: tk.Tk) -> None:
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Modul hinzufuegen")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.ergebnis: dict[str, object] | None = None

        self.kurs_id_var = tk.StringVar()
        self.kursname_var = tk.StringVar()
        self.ects_var = tk.StringVar()
        self.pruefungsform_var = tk.StringVar(value=Pruefungsform.KLAUSUR.value)
        self.note_var = tk.StringVar(value="")
        self.anerkannt_var = tk.BooleanVar(value=False)

        frame = ttk.Frame(self.dialog, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ID").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.kurs_id_var, width=14).grid(
            row=0, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Kursname").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.kursname_var, width=42).grid(
            row=1, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Pruefungsform").grid(row=2, column=0, sticky="w", pady=4)
        self.pruefungsform_combo = ttk.Combobox(
            frame,
            textvariable=self.pruefungsform_var,
            values=[pruefungsform.value for pruefungsform in Pruefungsform],
            state="readonly",
        )
        self.pruefungsform_combo.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0))
        ttk.Label(frame, text="ECTS").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.ects_var, width=8).grid(
            row=3, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Note").grid(row=4, column=0, sticky="w", pady=4)
        self.note_combo = ttk.Combobox(
            frame,
            textvariable=self.note_var,
            values=[""] + [str(note) for note in sorted(ERLAUBTE_NOTEN)],
            state="readonly",
        )
        self.note_combo.grid(row=4, column=1, sticky="ew", pady=4, padx=(8, 0))
        ttk.Checkbutton(
            frame,
            text="anerkannt",
            variable=self.anerkannt_var,
            command=self._anerkannt_geaendert,
        ).grid(row=5, column=1, sticky="w", pady=(6, 0), padx=(8, 0))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(button_frame, text="Abbrechen", command=self.dialog.destroy).pack(
            side="right",
            padx=(8, 0),
        )
        ttk.Button(button_frame, text="Speichern", command=self._speichern).pack(
            side="right"
        )

        frame.columnconfigure(1, weight=1)
        self.dialog.bind("<Return>", lambda _event: self._speichern())
        self.dialog.bind("<Escape>", lambda _event: self.dialog.destroy())
        popup_am_cursor_platzieren(self.dialog, parent)

    def anzeigen(self) -> dict[str, object] | None:
        self.dialog.wait_window()
        return self.ergebnis

    def _anerkannt_geaendert(self) -> None:
        state = "disabled" if self.anerkannt_var.get() else "readonly"
        self.pruefungsform_combo.configure(state=state)
        self.note_combo.configure(state=state)
        if self.anerkannt_var.get():
            self.note_var.set("")

    def _speichern(self) -> None:
        try:
            ects = int(self.ects_var.get())
        except ValueError:
            messagebox.showerror("Eingabe pruefen", "ECTS muessen eine ganze Zahl sein.")
            return

        kurs_id = self.kurs_id_var.get().strip()
        kursname = self.kursname_var.get().strip()
        if not kurs_id or not kursname:
            messagebox.showerror("Eingabe pruefen", "ID und Kursname sind Pflichtfelder.")
            return

        pruefungsform = self._pruefungsform_lesen()
        note = None
        if not self.anerkannt_var.get():
            note = None if self.note_var.get() == "" else float(self.note_var.get())

        self.ergebnis = {
            "kurs_id": kurs_id,
            "kursname": kursname,
            "ects": ects,
            "pruefungsform": pruefungsform,
            "ist_anerkannt": self.anerkannt_var.get(),
            "note": note,
        }
        self.dialog.destroy()

    def _pruefungsform_lesen(self) -> Pruefungsform:
        for pruefungsform in Pruefungsform:
            if pruefungsform.value == self.pruefungsform_var.get():
                return pruefungsform
        raise ValueError("Unbekannte Pruefungsform.")


class ModulBearbeitenDialog:
    def __init__(self, parent: tk.Tk, modul: ModulDaten) -> None:
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Bearbeiten")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.ergebnis: dict[str, object] | None = None
        self.modul = modul

        self.kurs_id_var = tk.StringVar(value=modul.kurs_id)
        self.kursname_var = tk.StringVar(value=modul.kursname)
        self.ects_var = tk.StringVar(value=str(modul.ects))
        self.pruefungsform_var = tk.StringVar(
            value=(
                Pruefungsform.KLAUSUR.value
                if modul.pruefungsform is None
                else modul.pruefungsform
            )
        )
        self.note_var = tk.StringVar(value="" if modul.note is None else str(modul.note))

        frame = ttk.Frame(self.dialog, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="ID").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.kurs_id_var).grid(
            row=0, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Kursname").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.kursname_var).grid(
            row=1, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Pruefungsform").grid(row=2, column=0, sticky="w", pady=4)
        self.pruefungsform_combo = ttk.Combobox(
            frame,
            textvariable=self.pruefungsform_var,
            values=[pruefungsform.value for pruefungsform in Pruefungsform],
            state="disabled" if modul.status == ModulStatus.ANERKANNT else "readonly",
        )
        self.pruefungsform_combo.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="ECTS").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(frame, textvariable=self.ects_var).grid(
            row=3, column=1, sticky="ew", pady=4, padx=(8, 0)
        )
        ttk.Label(frame, text="Note").grid(row=4, column=0, sticky="w", pady=4)
        self.note_combo = ttk.Combobox(
            frame,
            textvariable=self.note_var,
            values=self._notenwerte(),
            state="disabled" if modul.status == ModulStatus.ANERKANNT else "readonly",
        )
        self.note_combo.grid(row=4, column=1, sticky="ew", pady=4, padx=(8, 0))

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(button_frame, text="Abbrechen", command=self.dialog.destroy).pack(
            side="right",
            padx=(8, 0),
        )
        ttk.Button(button_frame, text="Speichern", command=self._speichern).pack(
            side="right",
            padx=(8, 0),
        )
        ttk.Button(button_frame, text="Modul loeschen", command=self._loeschen).pack(
            side="right"
        )

        frame.columnconfigure(1, weight=1)
        self.dialog.bind("<Return>", lambda _event: self._speichern())
        self.dialog.bind("<Escape>", lambda _event: self.dialog.destroy())
        popup_am_cursor_platzieren(self.dialog, parent)

    def anzeigen(self) -> dict[str, object] | None:
        self.dialog.wait_window()
        return self.ergebnis

    def _readonly_entry(self, parent: ttk.Frame, variable: tk.StringVar) -> ttk.Entry:
        return ttk.Entry(parent, textvariable=variable, state="readonly")

    def _notenwerte(self) -> list[str]:
        if self.modul.note is None:
            return [""] + [str(note) for note in sorted(ERLAUBTE_NOTEN)]
        return [str(note) for note in sorted(ERLAUBTE_NOTEN)]

    def _speichern(self) -> None:
        try:
            ects = int(self.ects_var.get())
        except ValueError:
            messagebox.showerror("Eingabe pruefen", "ECTS muessen eine ganze Zahl sein.")
            return

        kursname = self.kursname_var.get().strip()
        if not kursname:
            messagebox.showerror("Eingabe pruefen", "Der Kursname ist ein Pflichtfeld.")
            return

        note = None if self.note_var.get() == "" else float(self.note_var.get())
        self.ergebnis = {
            "typ": "speichern",
            "kursname": kursname,
            "ects": ects,
            "pruefungsform": self._pruefungsform_lesen(),
            "note": note,
        }
        self.dialog.destroy()

    def _loeschen(self) -> None:
        self.ergebnis = {"typ": "loeschen"}
        self.dialog.destroy()

    def _pruefungsform_lesen(self) -> Pruefungsform:
        for pruefungsform in Pruefungsform:
            if pruefungsform.value == self.pruefungsform_var.get():
                return pruefungsform
        raise ValueError("Unbekannte Pruefungsform.")
