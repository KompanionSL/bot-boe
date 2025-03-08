#!/bin/bash
echo "Instalando Chromium compatible..."
apt-get update && apt-get install -y chromium chromium-driver libglib2.0-0

echo "Ejecutando la aplicación..."
exec gunicorn bot_boe:app --timeout 120 --bind 0.0.0.0:$PORT
