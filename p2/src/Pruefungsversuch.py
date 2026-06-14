from dataclasses import dataclass


@dataclass(frozen=True)
class Pruefungsversuch:
    nummer: int
    note: float

    def __post_init__(self) -> None:
        if self.nummer < 1:
            raise ValueError("Die Versuchsnummer muss >= 1 sein.")
        if not 1.0 <= self.note <= 6.0:
            raise ValueError("Die Note muss zwischen 1.0 und 6.0 liegen.")
