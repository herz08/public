#!/bin/bash

# Logdatei definieren
LOGFILE="infoscreen.log"

# Virtuelle Umgebung aktivieren
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtuelle Umgebung wird aktiviert..." | tee -a $LOGFILE
source infoscreen/bin/activate

# Kurze Verzögerung
sleep 1

max_attempts=3
attempt=1
while (( attempt <= max_attempts ))
do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starte infoscreen.py (Versuch $attempt von $max_attempts)..." | tee -a $LOGFILE
    python3 infoscreen.py 2>&1 | tee -a $LOGFILE
    exit_code=$?

    # Prüfen, ob das Programm erfolgreich beendet wurde (Exit-Code 0)
    if [ $exit_code -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] infoscreen.py wurde erfolgreich beendet." | tee -a $LOGFILE
        break
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fehler: infoscreen.py beendet mit Exit-Code $exit_code. Warte 2 Sekunden und starte erneut..." | tee -a $LOGFILE
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
