# ============================================================
# MAPA INTERATIVO DO RODOANEL - TRECHO OESTE
# ============================================================
#
# OBJETIVO:
# Criar um mapa interativo do Rodoanel utilizando:
#
# - GeoJSON da rodovia
# - Folium
# - GeoPandas
#
# O mapa permite:
#
# ✔ Exibir o trecho Oeste
# ✔ Adicionar pontos coloridos
# ✔ Simular classificações
# ✔ Futuramente integrar IA/classificação automática
#
# ============================================================

# ============================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

import folium
import geopandas as gpd
import json

from shapely.geometry import box

# ============================================================
# 1. CARREGAR O ARQUIVO GEOJSON
# ============================================================
#
# Este arquivo contém:
# - geometria da rodovia
# - coordenadas
# - pontos ou linhas
#
# IMPORTANTE:
# O arquivo deve estar na mesma pasta do código.
#
# ============================================================

arquivo = "classificacao_rocada.geojson"

# Abrir GeoJSON
with open(arquivo, encoding="utf-8") as f:
    geojson_data = json.load(f)

# Ler arquivo usando GeoPandas
gdf = gpd.read_file(arquivo)

# Garantir sistema de coordenadas correto
gdf = gdf.to_crs(epsg=4326)

# ============================================================
# 2. CONFIGURAÇÃO DOS TRECHOS
# ============================================================
#
# Cada trecho possui:
#
# - limite oeste
# - limite leste
# - limite sul
# - limite norte
# - cor padrão
#
# Isso permite futuramente:
#
# ✔ adicionar novos trechos
# ✔ adicionar outras rodovias
# ✔ organizar o sistema
#
# ============================================================

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

# ============================================================
# 3. ESCOLHER O TRECHO ATUAL
# ============================================================
#
# Basta trocar:
#
# "OESTE"
# "SUL"
# "LESTE"
#
# ============================================================

TRECHO_ATUAL = TRECHOS["OESTE"]

# ============================================================
# 4. CRIAR ÁREA DE RECORTE (BOUNDING BOX)
# ============================================================
#
# O box define a área que será exibida.
#
# Tudo fora desses limites será removido.
#
# ============================================================

bbox = box(

    TRECHO_ATUAL["oeste"],
    TRECHO_ATUAL["sul"],

    TRECHO_ATUAL["leste"],
    TRECHO_ATUAL["norte"]
)

# ============================================================
# 5. RECORTAR O MAPA
# ============================================================
#
# Mantém apenas o trecho desejado.
#
# ============================================================

gdf_trecho = gdf.clip(bbox)

# ============================================================
# 6. MANTER SOMENTE A GEOMETRIA
# ============================================================
#
# Remove colunas desnecessárias.
#
# ============================================================

gdf_trecho = gdf_trecho[["geometry"]]

# ============================================================
# 7. SEPARAR MULTILINES
# ============================================================
#
# Alguns GeoJSON possuem linhas agrupadas.
#
# explode() separa tudo corretamente.
#
# ============================================================

gdf_trecho = gdf_trecho.explode(index_parts=False)

# ============================================================
# 8. FUNÇÃO DE CLASSIFICAÇÃO
# ============================================================
#
# Esta função converte:
#
# "baixa"  -> verde
# "media"  -> amarelo
# "alta"   -> vermelho
#
# FUTURAMENTE:
# outro código poderá alterar a classificação automaticamente.
#
# ============================================================

def definir_cor(classificacao):

    cores = {

        "baixa": "green",

        "media": "yellow",

        "alta": "red"
    }

    return cores.get(classificacao, "blue")

# ============================================================
# 9. CRIAR O MAPA
# ============================================================
#
# location:
# posição inicial do mapa
#
# zoom_start:
# nível de zoom inicial
#
# tiles:
# estilo visual do mapa
#
# ============================================================

mapa = folium.Map(

    location=[-23.58, -46.72],

    zoom_start=11,

    tiles="cartodbpositron"
)

# ============================================================
# 10. DESENHAR O TRECHO DA RODOVIA
# ============================================================
#
# Desenha a linha principal da rodovia.
#
# ============================================================

folium.GeoJson(

    gdf_trecho.__geo_interface__,

    name="Trecho Oeste",

    style_function=lambda x: {

        "color": TRECHO_ATUAL["cor"],

        "weight": 7,

        "opacity": 0.95
    }

).add_to(mapa)

# ============================================================
# 11. PONTOS MANUAIS DE TESTE
# ============================================================
#
# ESTES PONTOS SÃO TEMPORÁRIOS.
#
# Servem apenas para:
#
# ✔ testar as cores
# ✔ validar o sistema
# ✔ visualizar o mapa
#
# FUTURAMENTE:
# outro código irá gerar estes pontos automaticamente.
#
# ============================================================

pontos_teste = [

    # --------------------------------------------------------
    # PONTO VERMELHO
    # --------------------------------------------------------

    {
        "lat": -23.55,
        "lon": -46.82,
        "classificacao": "alta"
    },

    # --------------------------------------------------------
    # PONTO AMARELO
    # --------------------------------------------------------

    {
        "lat": -23.57,
        "lon": -46.78,
        "classificacao": "media"
    },

    # --------------------------------------------------------
    # PONTO VERDE
    # --------------------------------------------------------

    {
        "lat": -23.59,
        "lon": -46.74,
        "classificacao": "baixa"
    }
]

# ============================================================
# 12. DESENHAR OS PONTOS NO MAPA
# ============================================================
#
# Cada ponto:
#
# ✔ recebe uma cor
# ✔ recebe um popup
# ✔ é desenhado no mapa
#
# ============================================================

for ponto in pontos_teste:

    classificacao = ponto["classificacao"]

    cor = definir_cor(classificacao)

    folium.CircleMarker(

        # Coordenadas
        location=[ponto["lat"], ponto["lon"]],

        # Tamanho do ponto
        radius=15,

        # Cor da borda
        color=cor,

        # Preencher círculo
        fill=True,

        # Cor interna
        fill_color=cor,

        # Transparência
        fill_opacity=0.7,

        # Popup ao clicar
        popup=f"""
        Classificação: {classificacao}
        """

    ).add_to(mapa)

# ============================================================
# 13. CONTROLE DE CAMADAS
# ============================================================
#
# Adiciona botão de controle no canto do mapa.
#
# ============================================================

folium.LayerControl().add_to(mapa)

# ============================================================
# 14. SALVAR MAPA
# ============================================================
#
# Gera arquivo HTML interativo.
#
# Basta abrir no navegador.
#
# ============================================================

mapa.save("trecho_oeste_rodoanel.html")

# ============================================================
# 15. MENSAGEM FINAL
# ============================================================

print("Mapa gerado com sucesso!")
print("Arquivo salvo como: trecho_oeste_rodoanel.html")