#!/bin/bash

echo "🔧 Instalando dependencias necesarias..."
apt-get update && apt-get install -y wget unzip curl
apt-get install -y chromium-browser chromium-driver libglib2.0-0

echo "🌍 Instalando ChromeDriver manualmente..."
CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp/
unzip /tmp/chromedriver_linux64.zip -d /tmp/
chmod +x /tmp/chromedriver
mv /tmp/chromedriver /usr/local/bin/chromedriver

echo "🚀 Iniciando la aplicación..."
exec gunicorn bot_boe_selenium:app --timeout 120 --bind 0.0.0.0:$PORT
