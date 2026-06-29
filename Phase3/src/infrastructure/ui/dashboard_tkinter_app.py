import tkinter as tk
from tkinter import messagebox, ttk

from application.dtos.dashboard_daten_response import DashboardDatenResponse, ModulDaten
from application.dtos.studium_bearbeiten_requests import ModulBearbeitenRequest, ModulHinzufuegenRequest
from application.ports.studien_analyse_use_case import StudienAnalyseUseCase
from application.ports.studium_bearbeiten_use_case import StudiumBearbeitenUseCase
from domain.modul_status import ModulStatus
from infrastructure.ui.modul_dialoge import ModulBearbeitenDialog, ModulHinzufuegenDialog


class DashboardTkinterApp:
    KENNZAHL_BOX_HOEHE = 104
    UNGEPLANTE_ECTS_KEY = "UNGEPLANT"

    def __init__(
        self,
        analyse_port: StudienAnalyseUseCase,
        bearbeiten_port: StudiumBearbeitenUseCase,
    ) -> None:
        self.analyse_port = analyse_port
        self.bearbeiten_port = bearbeiten_port
        self.fenster = tk.Tk()
        self.fenster.title("Studien-Dashboard")
        self.fenster.geometry("1120x720")
        self._module: dict[str, ModulDaten] = {}
        self._sortierspalte: str | None = None
        self._sortierung_absteigend = False

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
            height=150,
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

        self._tabellen_ueberschriften = {
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
            "status": 170,
            "pruefungsform": 130,
            "note": 150,
        }

        for spalte in spalten:
            self.tabelle.heading(
                spalte,
                text=self._tabellen_ueberschriften[spalte],
                command=lambda sortierspalte=spalte: self._tabelle_sortieren(sortierspalte),
            )
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
                ModulHinzufuegenRequest(
                    kurs_id=modul["kurs_id"],
                    kursname=modul["kursname"],
                    ects=modul["ects"],
                    pruefungsform=modul["pruefungsform"],
                    note=modul["note"],
                    ist_anerkannt=modul["ist_anerkannt"],
                )
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
                ModulBearbeitenRequest(
                    kurs_id=modul.kurs_id,
                    kursname=aktion["kursname"],
                    ects=aktion["ects"],
                    pruefungsform=aktion["pruefungsform"],
                    note=aktion["note"],
                )
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

    def _kennzahlen_aktualisieren(self, daten: DashboardDatenResponse) -> None:
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
            text=(
                f"{daten.fortschritt_prozent} % fertig, {daten.offene_ects} ECTS offen\n"
                f"{daten.geplante_ects} geplant, {daten.ungeplante_ects} ungeplant"
            )
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

    def _donut_zeichnen(self, daten: DashboardDatenResponse) -> None:
        self.donut_canvas.delete("all")
        farben = self._donut_farben()
        werte = [
            (status, daten.ects_nach_status.get(status, 0))
            for status in (
                ModulStatus.ANERKANNT,
                ModulStatus.FERTIG,
                ModulStatus.IN_ARBEIT,
                ModulStatus.OFFEN,
            )
        ]
        werte.append((self.UNGEPLANTE_ECTS_KEY, daten.ungeplante_ects))
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

    def _legende_zeichnen(self, daten: DashboardDatenResponse) -> None:
        self.legende_canvas.delete("all")
        farben = self._donut_farben()
        eintraege = (
            (ModulStatus.ANERKANNT, "anerkannt"),
            (ModulStatus.FERTIG, "fertig"),
            (ModulStatus.IN_ARBEIT, "in Arbeit"),
            (ModulStatus.OFFEN, "geplant offen"),
            (self.UNGEPLANTE_ECTS_KEY, "ungeplant"),
        )
        for index, (status, beschriftung) in enumerate(eintraege):
            y = 14 + index * 28
            ects = self._ects_fuer_legenden_status(daten, status)
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
        sortierte_module = self._sortierte_module(module)
        self._module = {modul.kurs_id: modul for modul in sortierte_module}
        for eintrag in self.tabelle.get_children():
            self.tabelle.delete(eintrag)

        for modul in sortierte_module:
            self.tabelle.insert(
                "",
                "end",
                iid=modul.kurs_id,
                values=(
                    modul.kurs_id,
                    modul.ects,
                    modul.kursname,
                    "-" if modul.pruefungsform is None else modul.pruefungsform,
                    self._status_anzeigen(modul),
                    self._note_anzeigen(modul),
                ),
            )
        self._tabellenkopf_aktualisieren()

    def _tabelle_sortieren(self, spalte: str) -> None:
        if self._sortierspalte == spalte:
            self._sortierung_absteigend = not self._sortierung_absteigend
        else:
            self._sortierspalte = spalte
            self._sortierung_absteigend = False

        module = list(self._module.values())
        self._tabelle_aktualisieren(module)

    def _sortierte_module(self, module: list[ModulDaten]) -> list[ModulDaten]:
        if self._sortierspalte is None:
            return module

        return sorted(
            module,
            key=lambda modul: self._sortierwert(modul, self._sortierspalte),
            reverse=self._sortierung_absteigend,
        )

    def _sortierwert(self, modul: ModulDaten, spalte: str) -> object:
        if spalte == "kurs_id":
            return modul.kurs_id.lower()
        if spalte == "ects":
            return modul.ects
        if spalte == "kursname":
            return modul.kursname.lower()
        if spalte == "pruefungsform":
            return "" if modul.pruefungsform is None else modul.pruefungsform.lower()
        if spalte == "status":
            return modul.status.value.lower()
        if spalte == "note":
            if modul.note is not None:
                return modul.note
            if modul.versuche:
                return modul.versuche[-1].note
            return float("inf")
        return ""

    def _tabellenkopf_aktualisieren(self) -> None:
        for spalte, text in self._tabellen_ueberschriften.items():
            if spalte == self._sortierspalte:
                richtung = " v" if self._sortierung_absteigend else " ^"
                text = f"{text}{richtung}"
            self.tabelle.heading(
                spalte,
                text=text,
                command=lambda sortierspalte=spalte: self._tabelle_sortieren(sortierspalte),
            )

    def _status_anzeigen(self, modul: ModulDaten) -> str:
        if modul.status in (ModulStatus.IN_ARBEIT, ModulStatus.FERTIG):
            return f"{modul.status.value} ({len(modul.versuche)}/3)"
        return modul.status.value

    def _note_anzeigen(self, modul: ModulDaten) -> str:
        if modul.note is not None:
            return str(modul.note)
        if modul.versuche:
            letzter_versuch = modul.versuche[-1]
            return f"{letzter_versuch.note} (nicht bestanden)"
        return "-"

    def _zieltext(self, ziel_erreicht: bool | None) -> str:
        if ziel_erreicht is None:
            return "noch keine Note"
        if ziel_erreicht:
            return "erreicht"
        return "nicht erreicht"

    def _velocity_hinweis(self, daten: DashboardDatenResponse) -> str:
        if daten.ziel_velocity_ects_pro_monat <= daten.velocity_ects_pro_monat:
            return "erreicht"
        return "nicht erreicht"

    def _prognose_hinweis(self, daten: DashboardDatenResponse) -> str:
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

    def _donut_farben(self) -> dict[ModulStatus | str, str]:
        farben: dict[ModulStatus | str, str] = self._status_farben()
        farben[self.UNGEPLANTE_ECTS_KEY] = "#e6e6e6"
        return farben

    def _ects_fuer_legenden_status(
        self,
        daten: DashboardDatenResponse,
        status: ModulStatus | str,
    ) -> int:
        if status == self.UNGEPLANTE_ECTS_KEY:
            return daten.ungeplante_ects
        return daten.ects_nach_status.get(status, 0)
