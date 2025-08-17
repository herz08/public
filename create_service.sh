#!/bin/bash

SERVICE_PATH="/etc/systemd/system/startscreen.service"

cat <<EOF | sudo tee "$SERVICE_PATH" > /dev/null
[Unit]
Description=Startscript Infoscreen
After=network.target

[Service]
WorkingDirectory=/home/pi
ExecStart=/home/pi/start_infoscreen.sh
Restart=on-failure
User=pi

[Install]
WantedBy=multi-user.target
EOF

echo "Service-Datei wurde erstellt: $SERVICE_PATH"

echo "systemctl deamon-reload und enable wird ausgeführt..."
sudo systemctl daemon-reload
sudo systemctl enable startscreen.service
echo "Service wurde aktiviert."
sudo systemctl start startscreen.service
echo "Service wurde gestartet."
echo "Status des Services:"
sudo systemctl status startscreen.service