#!/bin/bash

# Virtuelle Umgebung aktivieren
source infoscreen/bin/activate

# Kurze Verzögerung
sleep 1

# Versuche, das Python-Skript bis zu 3 Mal zu starten, falls Fehler auftreten
max_attempts=3
attempt=1
while (( attempt <= max_attempts ))
do
    python3 infoscreen.py && break
    echo "Start fehlgeschlagen, Versuch $attempt von $max_attempts. Warte 2 Sekunden..."
    sleep 2
    ((attempt++))
done

# Virtuelle Umgebung deaktivieren (optional)
deactivate
