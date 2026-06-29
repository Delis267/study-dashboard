# Phase 2 - Testprogramme starten

Im Ordner `Phase2` ausführen:

```powershell
python run_tests.py
```

Das startet die OOP-Tests und den JSON-Repository-Test.
Ab Phase2 sind die Tests jeweils Python-Module, da sie voneinander abhängen.

Einzelne Tests können optional separat gestartet werden:

```powershell
cd src
python -m oo_test.main
python -m repo_test.main
```
