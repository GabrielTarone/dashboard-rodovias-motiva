import folium
import geopandas as gpd
import numpy as np
import json
from folium.plugins import HeatMap

# =========================================
# 1. CARREGAR ARQUIVO
# =========================================

arquivo = "rodoanel.json"

with open(arquivo, encoding="utf-8") as f:
    geojson_data = json.load(f)

gdf = gpd.read_file(arquivo)
gdf = gdf.to_crs(epsg=4326)

# =========================================
# 2. GERAR PONTOS AO LONGO DAS LINHAS
# =========================================

pontos = []

for _, row in gdf.iterrows():
    geom = row.geometry

    if geom.geom_type == "LineString":
        coords = list(geom.coords)

        for coord in coords:
            lat = coord[1]
            lon = coord[0]

            # intensidade simulada
            intensidade = np.random.randint(1, 10)

            pontos.append([lat, lon, intensidade])

    elif geom.geom_type == "MultiLineString":
        for linha in geom.geoms:
            coords = list(linha.coords)

            for coord in coords:
                lat = coord[1]
                lon = coord[0]

                intensidade = np.random.randint(1, 10)

                pontos.append([lat, lon, intensidade])

# =========================================
# 3. CRIAR MAPA
# =========================================

mapa = folium.Map(
    location=[-23.55, -46.63],
    zoom_start=11,
    tiles="cartodbpositron"
)

# =========================================
# 4. DESENHAR RODOANEL (BASE)
# =========================================

folium.GeoJson(
    geojson_data,
    name="Rodoanel",
    style_function=lambda x: {
        "color": "blue",
        "weight": 4,
        "opacity": 0.8
    }
).add_to(mapa)

# =========================================
# 5. HEATMAP POR CIMA DAS LINHAS
# =========================================

HeatMap(
    pontos,
    name="Intensidade de Manutenção",
    radius=12,
    blur=18,
    gradient={
        0.2: 'green',
        0.5: 'yellow',
        0.8: 'orange',
        1.0: 'red'
    }
).add_to(mapa)

# =========================================
# 6. CONTROLE DE CAMADAS
# =========================================

folium.LayerControl().add_to(mapa)

# =========================================
# 7. SALVAR
# =========================================

mapa.save("mapa_rodoanel_heatmap.html")

print("Mapa gerado com sucesso!")