class Pruefungsleistung:
    def __init__(self, note: float, versuch: int):

        if not 1.0 <= note <= 6.0:
            raise ValueError("Die Note muss zwischen 1.0 und 6.0 liegen.")
        if not 1 <= versuch <= 3:
            raise ValueError("Es kann nur 1-3 Versuche für eine Prüfungsleistung geben.")

        self.note = note
        self.versuch = versuch


    @property
    def ist_bestanden(self) -> bool:
        return self.note <= 4.0

    def __repr__(self):
        return f"Prüfungsleistung(note={self.note!r}, versuch={self.versuch})"