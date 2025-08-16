#!/bin/bash

# Logdatei definieren
LOGFILE="infoscreen.log"

# Virtuelle Umgebung aktivieren
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtuelle Umgebung wird aktiviert..." | tee -a $LOGFILE
source infoscreen/bin/activate

# Kurze Verzögerung
sleep 1

# Versuche, das Python-Skript bis zu 3 Mal zu starten, falls Fehler auftreten
max_attempts=3
attempt=1
while (( attempt <= max_attempts ))
do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Versuche, infoscreen.py zu starten (Versuch $attempt von $max_attempts)..." | tee -a $LOGFILE
    python3 infoscreen.py >> $LOGFILE 2>&1
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Erfolg: infoscreen.py wurde erfolgreich gestartet!" | tee -a $LOGFILE
        break
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fehler: Start fehlgeschlagen. Warte 2 Sekunden und starte erneut..." | tee -a $LOGFILE
        sleep 2
        ((attempt++))
    fi
done

if (( attempt > max_attempts )); then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fehler: Alle Startversuche fehlgeschlagen." | tee -a $LOGFILE
fi

# Virtuelle Umgebung deaktivieren (optional)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtuelle Umgebung wird deaktiviert..." | tee -a $LOGFILE
deactivate
