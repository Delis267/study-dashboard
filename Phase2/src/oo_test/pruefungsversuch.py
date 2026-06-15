from dataclasses import dataclass


@dataclass(frozen=True)
class Pruefungsversuch:
    note: float

    def __post_init__(self) -> None:
        if not 1.0 <= self.note <= 6.0:
            raise ValueError("Die Note muss zwischen 1.0 und 6.0 liegen.")

    @property
    def ist_bestanden(self) -> bool:
        return self.note <= 4.0

    def __str__(self) -> str:
        return f"(note={self.note}, bestanden={self.ist_bestanden})"
