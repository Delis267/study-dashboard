from dataclasses import dataclass


ERLAUBTE_NOTEN = {
    1.0,
    1.3,
    1.7,
    2.0,
    2.3,
    2.7,
    3.0,
    3.3,
    3.7,
    4.0,
    5.0,
}


@dataclass(frozen=True)
class Pruefungsversuch:
    note: float

    def __post_init__(self) -> None:
        if self.note not in ERLAUBTE_NOTEN:
            raise ValueError("Die Note ist fachlich nicht zulaessig.")

    @property
    def ist_bestanden(self) -> bool:
        return self.note <= 4.0

    def __str__(self) -> str:
        return f"Pruefungsversuch(note={self.note}, bestanden={self.ist_bestanden})"

    def __repr__(self) -> str:
        return str(self)

