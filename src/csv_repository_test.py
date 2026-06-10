import csv
import os

class CsvModulRepository:
    def __init__(self, dateiname):
        self.dateiname = dateiname
        self.header = ["id", "titel"]

        ordner = os.path.dirname(self.dateiname)
        if ordner != "":
            os.makedirs(ordner, exist_ok=True)

        if not os.path.exists(self.dateiname):
            with open(self.dateiname, "w", newline="", encoding="utf-8") as datei:
                writer = csv.DictWriter(datei, fieldnames=self.header)
                writer.writeheader()

    def createModul(self, id, titel):
        with open(self.dateiname, "a", newline="", encoding="utf-8") as datei:
            writer = csv.DictWriter(datei, fieldnames=self.header)
            writer.writerow({"id": id, "titel": titel})

    def printAllModuls(self):
        print(f"Lesen der Module aus {self.dateiname}...")
        with open(self.dateiname, "r", encoding="utf-8") as datei:
            reader = csv.DictReader(datei)
            module = list(reader)
            
            for modul in module:
                print(modul)

        return module

    # Loescht ein Modul anhand der ID indem es alles löscht und ohne das Modul mit der ID neu schreibt
    def deleteModulById(self, id):
        module = self.printAllModuls()

        with open(self.dateiname, "w", newline="", encoding="utf-8") as datei:
            writer = csv.DictWriter(datei, fieldnames=self.header)
            writer.writeheader()

            for modul in module:
                if modul["id"] != str(id):
                    writer.writerow(modul)


# Kleiner Testablauf fuer Phase 1
repo = CsvModulRepository("data/module_database.csv")

print("Modul anlegen")
repo.createModul("TEST01", "Testmodul")
repo.createModul("TEST02", "Testmodul2")
repo.createModul("TEST03", "Testmodul3")
print("Alle Module:")
repo.printAllModuls()

print("Modul wieder loeschen")
repo.deleteModulById("TEST01")

print("Alle Module nach dem Loeschen:")
repo.printAllModuls()
