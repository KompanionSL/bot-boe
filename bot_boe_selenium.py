from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, request
import time

app = Flask(__name__)

def buscar_en_boe_selenium(consulta):
    url = f"https://www.boe.es/buscar/boe.php?campo%5B0%5D=TIT&dato%5B0%5D={consulta}&page_hits=3"
    
    # Configuración del navegador en modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    
    time.sleep(3)  # Esperar que cargue el contenido dinámico
    
    resultados = driver.find_elements(By.CLASS_NAME, "resultado_boe")
    
    if resultados:
        respuesta = "🔎 Resultados en BOE:\n"
        for resultado in resultados[:3]:  
            titulo = resultado.find_element(By.TAG_NAME, "h3").text.strip()
            link = resultado.find_element(By.TAG_NAME, "a").get_attribute("href")
            respuesta += f"\n📌 {titulo}\n🔗 {link}\n"
        
        driver.quit()
        return respuesta
    else:
        driver.quit()
        return "❌ No encontré información en el BOE sobre este tema."

@app.route("/")
def home():
    return "El bot del BOE con Selenium está funcionando."

@app.route("/buscar", methods=["GET"])
def buscar():
    consulta = request.args.get("q")
    if not consulta:
        return "⚠️ Debes proporcionar una consulta. Ejemplo: /buscar?q=impuestos"
    return buscar_en_boe_selenium(consulta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
