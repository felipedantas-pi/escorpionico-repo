import pandas as pd
import geopandas as gpd
import requests
import zipfile
import os
import matplotlib.pyplot as plt
import mapclassify
from io import BytesIO
from pypalettes import load_cmap
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyArrowPatch
from highlight_text import fig_text, ax_text

# Arquivo shapefile dos limites dos estados brasileiros
url_ibge_brasil = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_unidades_da_federacao.zip"

# Nome do arquivo dentro do ZIP que você deseja carregar
arquivo_vetorial = 'BR_UF_2019.shp'

# Função para baixar e descompactar o arquivo ZIP
def baixar_e_descompactar(url, diretorio_destino):
    response = requests.get(url)
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(diretorio_destino)
        # Listar todos os arquivos descompactados
        print("Arquivos no ZIP:")
        zip_ref.printdir()

# Diretório temporário para armazenar os arquivos descompactados
diretorio = '../data/ibge/malha_territorial/'

# Criar o diretório temporário se não existir
os.makedirs(diretorio, exist_ok=True)

# Baixar e descompactar o arquivo ZIP
baixar_e_descompactar(url_ibge_brasil, diretorio)

# Listar os arquivos descompactados para encontrar o arquivo vetorial
for root, dirs, files in os.walk(diretorio):
    for file in files:
        print(os.path.join(root, file))

# Caminho completo do arquivo vetorial descompactado
caminho_arquivo_vetorial = os.path.join(diretorio, arquivo_vetorial)

# Carregar o arquivo vetorial com geopandas
brasil_uf = gpd.read_file(caminho_arquivo_vetorial)

# Carregar arquivo agregado stats
ii = pd.read_csv('../data/dataset_amostra_stats_media_uf.csv')

brasil_uf['CD_UF'] = brasil_uf['CD_UF'].astype(str)
ii['coduf'] = ii['coduf'].astype(str)

gdf = brasil_uf.merge(ii, left_on='CD_UF', right_on='coduf')

# Seelcionando colunas desejadas
gdf = gdf[['CD_UF',
 'NM_UF',
 'SIGLA_UF',
 'NM_REGIAO',
 'ii_09',
 'ii_19',
 'ii_variacao_percentual',
 'geometry']


# load colormap
cmap = load_cmap('BrwnYl', type='continuous')

# Classificação Jenks
nb5 = mapclassify.NaturalBreaks(gdf['ii_09'], k=5)

# initialize the figure
fig, ax = plt.subplots(figsize=(15, 15), dpi=300)
# create the plot
gdf.plot(ax=ax, column='ii_09', cmap=cmap, k=5, edgecolor='black', linewidth=0.5, legend=True)
# custom axis
ax.set_xlim(-80, -30)
ax.set_ylim(-35,6)
#plt.show()

# Mapa Coroplético
mapping = dict([(i, s) for i, s in enumerate(nb5.get_legend_classes())])

def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)


ax.set_axis_off()
replace_legend_items(ax.get_legend(), mapping)