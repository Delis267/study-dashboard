from enum import Enum

class ModulStatus(Enum):
    OFFEN = "Offen"
    IN_ARBEIT = "In Arbeit"
    FERTIG = "Fertig"
    ANERKANNT = "Anerkannt"

    def __str__(self) -> str:
        return self.name