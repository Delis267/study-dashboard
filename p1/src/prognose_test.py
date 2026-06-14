from datetime import date


# Machbarkeitstest Phase 1:
# Die Kennzahlen werden dynamisch aus wenigen stabilen Parametern berechnet.
# Sie werden nicht statisch gespeichert.

startdatum = date(2024, 3, 1)
heute = date.today()

ziel_ects = 180
regelstudienzeit_monate = 36
selbst_erarbeitete_ects = 105
anerkannte_ects = 15


def berechne_studierte_monate(start, ende):
    monate = (ende.year - start.year) * 12 + ende.month - start.month

    if ende.day >= start.day:
        monate = monate + 1

    if monate < 1:
        monate = 1

    return monate


def addiere_monate(start, monate):
    jahr = start.year + (start.month - 1 + monate) // 12
    monat = (start.month - 1 + monate) % 12 + 1

    return date(jahr, monat, 1)


studierte_monate = berechne_studierte_monate(startdatum, heute)

abgeschlossene_ects = selbst_erarbeitete_ects + anerkannte_ects
offene_ects = ziel_ects - abgeschlossene_ects

# Anerkannte ECTS zaehlen zum Fortschritt, aber nicht zur Velocity.
velocity = selbst_erarbeitete_ects / studierte_monate
ziel_velocity = ziel_ects / regelstudienzeit_monate

if velocity > 0:
    prognose_restmonate = offene_ects / velocity
else:
    prognose_restmonate = 0

prognose_gesamtmonate = studierte_monate + prognose_restmonate
prognose_enddatum = addiere_monate(startdatum, round(prognose_gesamtmonate))

print("Prognose-Test Studien-Dashboard")
print("-------------------------------")
print("Startdatum:", startdatum)
print("Heutiges Datum:", heute)
print("Ende Regelstudienzeit:", addiere_monate(startdatum, regelstudienzeit_monate))
print("Ziel-ECTS:", ziel_ects)
print("Studierte Monate:", studierte_monate)
print("Selbst erarbeitete ECTS:", selbst_erarbeitete_ects)
print("Anerkannte ECTS:", anerkannte_ects)
print("Abgeschlossene ECTS:", abgeschlossene_ects)
print("Offene ECTS:", offene_ects)
print()
print("Berechnete Kennzahlen")
print("---------------------")
print("Velocity:", round(velocity, 2), "ECTS pro Monat")
print("Ziel-Velocity:", round(ziel_velocity, 2), "ECTS pro Monat")
print("Prognose Restmonate:", round(prognose_restmonate, 1))
print("Prognose Gesamtstudienzeit:", round(prognose_gesamtmonate, 1), "Monate")
print("Voraussichtliches Ende:", prognose_enddatum.strftime("%m.%Y"))

if prognose_gesamtmonate <= regelstudienzeit_monate:
    print("Status: innerhalb der Regelstudienzeit")
else:
    monate_hinter_plan = prognose_gesamtmonate - regelstudienzeit_monate
    print("Status:", round(monate_hinter_plan, 1), "Monate hinter Plan")
