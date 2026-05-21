from datetime import date


# Beispielwerte fuer den Machbarkeitstest
startdatum = date(2024, 10, 1)
heute = date.today()

ziel_ects = 180
ziel_monate = 36
selbst_erarbeitete_ects = 60
anerkannte_ects = 20
workload_pro_ects = 30

# Monate seit Studienstart berechnen
studierte_monate = (heute.year - startdatum.year) * 12 + (heute.month - startdatum.month)

if heute.day >= startdatum.day:
    studierte_monate = studierte_monate + 1

if studierte_monate < 1:
    studierte_monate = 1

# Einfache Kennzahlen berechnen
abgeschlossene_ects = selbst_erarbeitete_ects + anerkannte_ects
offene_ects = ziel_ects - abgeschlossene_ects

# Anerkannte ECTS zaehlen zum Fortschritt, aber nicht zur Velocity.
ects_pro_monat = selbst_erarbeitete_ects / studierte_monate
ziel_ects_pro_monat = ziel_ects / ziel_monate

if ects_pro_monat > 0:
    prognose_restmonate = offene_ects / ects_pro_monat
else:
    prognose_restmonate = 0

restworkload_stunden = offene_ects * workload_pro_ects

print("Studien-Dashboard Prognose-Test")
print("-------------------------------")
print("Startdatum:", startdatum)
print("Heutiges Datum:", heute)
print("Studierte Monate:", studierte_monate)
print("Ziel-ECTS:", ziel_ects)
print("Abgeschlossene ECTS:", abgeschlossene_ects)
print("Davon selbst erarbeitet:", selbst_erarbeitete_ects)
print("Davon anerkannt:", anerkannte_ects)
print("Offene ECTS:", offene_ects)
print("ECTS pro Monat ohne anerkannte Module:", round(ects_pro_monat, 2))
print("Ziel-ECTS pro Monat:", round(ziel_ects_pro_monat, 2))
print("Prognose Restmonate:", round(prognose_restmonate, 1))
print("Restworkload in Stunden:", restworkload_stunden)
