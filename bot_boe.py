import os  # 🔹 Asegúrate de agregar esta línea
from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def buscar_en_boe(consulta):
    url = f"https://www.boe.es/buscar/boe.php?campo%5B0%5D=TIT&dato%5B0%5D={consulta}&page_hits=3"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        resultados = soup.find_all("div", class_="resultado_boe")

        if resultados:
            respuesta = "🔎 Resultados en BOE:\n"
            for resultado in resultados[:3]:  
                titulo = resultado.find("h3").text.strip()
                link = "https://www.boe.es" + resultado.find("a")["href"]
                respuesta += f"\n📌 {titulo}\n🔗 {link}\n"
            return respuesta
        else:
            return "❌ No encontré información en el BOE sobre este tema."
    else:
        return "❌ Error al acceder al BOE."

@app.route("/")
def home():
    return "El bot del BOE está funcionando."

@app.route("/buscar", methods=["GET"])
def buscar():
    consulta = request.args.get("q")
    if not consulta:
        return "⚠️ Debes proporcionar una consulta. Ejemplo: /buscar?q=impuestos"
    return buscar_en_boe(consulta)

# 🔹 Ajuste para que funcione en Railway con el puerto correcto
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Usa el puerto de Railway si está definido
    app.run(host="0.0.0.0", port=port)
