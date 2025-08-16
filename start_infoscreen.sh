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
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starte infoscreen.py im Hintergrund (Versuch $attempt von $max_attempts)..." | tee -a $LOGFILE
    python3 infoscreen.py >> $LOGFILE 2>&1 &
    PY_PID=$!

    # Kurze Wartezeit, um zu prüfen, ob der Prozess sofort wieder beendet wurde (Fehler)
    sleep 2

    # Prüfen, ob der Prozess noch läuft
    if ps -p $PY_PID > /dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Erfolg: infoscreen.py läuft im Hintergrund (PID $PY_PID)." | tee -a $LOGFILE
        break
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Fehler: infoscreen.py konnte nicht gestartet werden. Warte 2 Sekunden und starte erneut..." | tee -a $LOGFILE
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
