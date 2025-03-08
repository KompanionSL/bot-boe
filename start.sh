#!/bin/bash
echo "Instalando Chromium y ChromeDriver..."
apt-get update && apt-get install -y chromium-browser chromium-driver

echo "Ejecutando la aplicación..."
gunicorn bot_boe_selenium:app --timeout 120 --bind 0.0.0.0:$PORT
