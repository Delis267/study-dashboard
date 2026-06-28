import tkinter as tk
from tkinter import messagebox, ttk

from application.dtos.dashboard_daten_response import ModulDaten
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
            value="-" if modul.pruefungsform is None else modul.pruefungsform
        )
        self.note_var = tk.StringVar(
            value=(
                "anerkannt"
                if modul.status == ModulStatus.ANERKANNT
                else "" if modul.note is None else str(modul.note)
            )
        )

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
        self.pruefungsform_combo.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0))
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
        ttk.Button(button_frame, text="Löschen", command=self._loeschen).pack(
            side="right"
        )

        frame.columnconfigure(1, weight=1)
        self.dialog.bind("<Return>", lambda _event: self._speichern())
        self.dialog.bind("<Escape>", lambda _event: self.dialog.destroy())
        popup_am_cursor_platzieren(self.dialog, parent)

    def anzeigen(self) -> dict[str, object] | None:
        self.dialog.wait_window()
        return self.ergebnis

    def _notenwerte(self) -> list[str]:
        if not self.modul.versuche or self.modul.note is None:
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

        note = (
            None
            if self.modul.status == ModulStatus.ANERKANNT or self.note_var.get() == ""
            else float(self.note_var.get())
        )
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
