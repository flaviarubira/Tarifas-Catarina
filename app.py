from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Caminho dos arquivos Excel
AERONAVES_FILE = "2025-01.xls"
TARIFAS_FILE = "Tarifas-2025.xlsx"

# Função para determinar a categoria com base no peso
def definir_categoria(peso):
    categorias = [
        (0, 1000, "I"),
        (1000, 2000, "II"),
        (2000, 4000, "III"),
        (4000, 6000, "IV"),
        (6000, 12000, "V"),
        (12000, 24500, "VI"),
        (24500, 48000, "VII"),
        (48000, 100000, "VIII"),
    ]
    for min_peso, max_peso, categoria in categorias:
        if min_peso <= peso < max_peso:
            return categoria
    return "Desconhecida"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        marca = request.form.get("marca")

        # Carregar os dados das aeronaves e tarifas
        aeronaves_df = pd.read_excel(AERONAVES_FILE)
        tarifas_df = pd.read_excel(TARIFAS_FILE)

        # Busca pela marca
        aeronave = aeronaves_df[aeronaves_df["MARCA"] == marca].iloc[0]
        modelo = aeronave["CD_TIPO_ICAO"]
        peso = aeronave["NR_PMD"]
        categoria = definir_categoria(peso)

        # Busca pelas tarifas da categoria
        tarifas = tarifas_df[tarifas_df["CATEGORIA"] == categoria].iloc[0].to_dict()

        return jsonify({
            "marca": marca,
            "modelo": modelo,
            "peso": peso,
            "categoria": categoria,
            "tarifas": tarifas,
        })

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
