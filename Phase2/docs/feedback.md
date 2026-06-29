# Feedback Ende Phase2

Die Reflexion ist fachlich fundiert, sehr gut strukturiert und zeigt eine nachvollziehbare Weiterentwicklung des Modells aus Phase 1. Besonders positiv ist, dass Modellierungsentscheidungen anhand konkreter Umsetzungsprobleme begründet werden und mehrere Alternativen diskutiert werden. Die Wahl von Enums, Properties, Dataclasses sowie die Verlagerung der Prüfungslogik in die Klasse Pruefungsleistung sind nachvollziehbar begründet und verbessern die Kapselung.
Anmerkungen zur Reflexion

    Die Entscheidung für @property bei ist_bestanden ist sinnvoll. Im UML ist dies jedoch als Eigenschaft modelliert, während in der Reflexion von einer zuvor geplanten Methode gesprochen wird. Die Unterscheidung zwischen abgeleitetem Attribut und Methode könnte noch präziser erläutert werden.
    Die Verwendung von @dataclass(frozen=True) wird nachvollziehbar begründet. Gleichzeitig sollte bedacht werden, dass spätere Korrekturen von Prüfungsdaten dadurch erschwert werden. Die Vor- und Nachteile könnten noch etwas stärker reflektiert werden.
    Der zulässige Notenbereich von 1,0 bis 6,0 erscheint nicht passend. Es werden nur bestimmte Notenstufen vergeben (z. B. 1,0 bis 4,0 in festgelegten Abstufungen sowie 5,0 für „nicht bestanden“). Werte wie 4,3, 5,7 oder 6,0 wären fachlich nicht plausibel. Die erlaubten Notenwerte sollten daher genauer modelliert und validiert werden, beispielsweise über eine definierte Menge zulässiger Noten oder eine entsprechende fachliche Regel.

Anmerkungen zum Gesamt-UML

    Die Architektur orientiert sich nachvollziehbar an einer vereinfachten Ports-and-Adapters-Architektur und trennt Domäne, Anwendungsschicht und Persistenz sauber. Dies geht deutlich über die Minimalanforderungen der Phase hinaus.
    Die Klasse StudienDashboardService übernimmt sämtliche Anwendungsfälle des Systems. Für den aktuellen Umfang ist dies vertretbar. Bei einer Erweiterung um weitere Dashboard-Funktionen (Velocity, Prognose, Notendurchschnitt, Auswertungen) besteht jedoch die Gefahr einer zu umfangreichen Service-Klasse. Die in der Reflexion erwähnte spätere Aufteilung in spezialisierte Use-Case-Services wäre dann sinnvoll.
    Die geplanten Dashboard-Kennzahlen aus Tabelle 1 sind im Domänenmodell bislang nur teilweise sichtbar. Velocity, Prognose und Notendurchschnitt werden in der Architektur beschrieben, besitzen jedoch noch keine erkennbaren fachlichen Klassen oder Services. Für die spätere Umsetzung sollte klar definiert werden, in welcher Schicht diese Berechnungen verankert werden.
    Die JSON-Struktur in Abbildung 3 speichert Prüfungsversuche lediglich als Liste von Noten. Im UML existiert jedoch die eigene Klasse Pruefungsversuch. Dadurch geht in der Persistenz ein Teil der Modellstruktur verloren. Langfristig wäre eine direkte Abbildung der Pruefungsversuch-Objekte konsistenter.
    Eine Application-Klasse als Composition Root fehlt in der dargestellten Gesamtarchitektur. Eine zentrale Klasse zum Verdrahten von GUI, Service und Repository würde die Architektur vervollständigen.

Starke Phase-2-Abgabe! 