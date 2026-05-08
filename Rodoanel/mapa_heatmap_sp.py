import folium
import geopandas as gpd
import numpy as np
import json

from shapely.geometry import box
from folium.plugins import HeatMap

# =========================================
# 1. CARREGAR ARQUIVO GEOJSON
# =========================================

arquivo = "rodoanel.json"

with open(arquivo, encoding="utf-8") as f:
    geojson_data = json.load(f)

gdf = gpd.read_file(arquivo)

# Garantir coordenadas em latitude/longitude
gdf = gdf.to_crs(epsg=4326)

# =========================================
# 2. CONFIGURAÇÃO DO TRECHO OESTE
# =========================================
# CONFIGURAÇÃO DOS TRECHOS
# =========================================

TRECHOS = {

    "OESTE": {
        "oeste": -46.84,
        "leste": -46.73,
        "sul": -23.63,
        "norte": -23.415,
        "cor": "blue"
    },

    "SUL": {
        "oeste": -46.73,
        "leste": -46.55,
        "sul": -23.80,
        "norte": -23.63,
        "cor": "green"
    },

    "LESTE": {
        "oeste": -46.55,
        "leste": -46.35,
        "sul": -23.65,
        "norte": -23.40,
        "cor": "red"
    }

}
# =========================================
# 3. CRIAR ÁREA DE RECORTE
# =========================================

TRECHO_ATUAL = TRECHOS["OESTE"]

bbox = box(
    TRECHO_ATUAL["oeste"],
    TRECHO_ATUAL["sul"],
    TRECHO_ATUAL["leste"],
    TRECHO_ATUAL["norte"]
)

# =========================================
# 4. RECORTAR O MAPA
# =========================================

gdf_trecho = gdf.clip(bbox)

# manter apenas geometria
gdf_trecho = gdf_trecho[["geometry"]]

# =========================================
# 5. SEPARAR MULTILINES
# =========================================

gdf_trecho = gdf_trecho.explode(index_parts=False)

# =========================================
# 6. GERAR PONTOS DE HEATMAP
# =========================================

pontos = []

for _, row in gdf_trecho.iterrows():

    geom = row.geometry

    if geom.geom_type == "LineString":

        coords = list(geom.coords)

        for coord in coords:

            lat = coord[1]
            lon = coord[0]

            # Intensidade simulada
            intensidade = np.random.randint(1, 10)

            pontos.append([lat, lon, intensidade])

# =========================================
# 8. CRIAR MAPA
# =========================================

mapa = folium.Map(
    location=[-23.58, -46.72],
    zoom_start=11,
    tiles="cartodbpositron"
)

# =========================================
# 9. DESENHAR TRECHO OESTE
# =========================================

folium.GeoJson(
    gdf_trecho.__geo_interface__,
    name="Trecho Oeste",
    style_function=lambda x: {
        "color": "blue",
        "weight": 7,
        "opacity": 0.95
    }
).add_to(mapa)

# =========================================
# 10. HEATMAP SOBRE A RODOVIA
# =========================================

HeatMap(
    pontos,
    name="Necessidade de Manutenção",
    radius=12,
    blur=18,
    gradient={
        0.2: "green",
        0.5: "yellow",
        0.8: "orange",
        1.0: "red"
    }
).add_to(mapa)

# =========================================
# 11. CONTROLE DE CAMADAS
# =========================================

folium.LayerControl().add_to(mapa)

# =========================================
# 12. SALVAR MAPA
# =========================================

mapa.save("trecho_oeste_rodoanel.html")

print("Mapa gerado com sucesso!")
print("Arquivo salvo como: trecho_oeste_rodoanel.html")