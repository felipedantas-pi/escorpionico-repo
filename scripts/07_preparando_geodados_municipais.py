# Importação das bibliotecas
# Dados
import pandas as pd
import geopandas as gpd

# Requisições
import os
import requests
import zipfile

from io import BytesIO

# URL FTP do arquivo .ZIP dos limites dos municípios brasileiros para 2019/2020
URL_BRASIL_MUNICIPIOS  = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2019/Brasil/BR/br_municipios_20200807.zip"

# Nome do arquivo dentro do ZIP que você deseja carregar
ARQUIVO_VETORIAL  = 'BR_Municipios_2019.shp'

def baixar_e_descompactar(url, diretorio_destino):
    """
    Baixa e descompacta um arquivo ZIP a partir de uma URL.
    
    Parameters:
    url (str): URL do arquivo ZIP.
    diretorio_destino (str): Diretório onde os arquivos serão descompactados.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(diretorio_destino)
    except requests.RequestException as e:
        print(f"Erro ao baixar o arquivo: {e}")
    except zipfile.BadZipFile as e:
        print(f"Erro ao descompactar o arquivo: {e}")
        
def listar_arquivos(diretorio):
    """
    Lista todos os arquivos em um diretório.
    
    Parameters:
    diretorio (str): Diretório onde os arquivos estão localizados.
    
    Returns:
    List[str]: Lista com os caminhos completos dos arquivos.
    """
    arquivos = []
    for root, _, files in os.walk(diretorio):
        for file in files:
            arquivos.append(os.path.join(root, file))
    return arquivos

# Diretório temporário para armazenar os arquivos descompactados
DIRETORIO_TEMPORARIO  = '../data/ibge/malha_territorial/'

# Verifica se o diretório temporário já existe
if os.path.exists(DIRETORIO_TEMPORARIO):
    print(f"Aviso: O diretório '{DIRETORIO_TEMPORARIO}' já existe.")
else:
    print(f"Criando o diretório '{DIRETORIO_TEMPORARIO}'.")
    os.makedirs(DIRETORIO_TEMPORARIO, exist_ok=True)

# Baixar e descompactar o arquivo ZIP
baixar_e_descompactar(URL_BRASIL_MUNICIPIOS, DIRETORIO_TEMPORARIO)

# Lista os arquivos descompactados para encontrar o arquivo vetorial
arquivos_descompactados = listar_arquivos(DIRETORIO_TEMPORARIO)
for arquivo in arquivos_descompactados:
    print(arquivo)

# Caminho completo do arquivo vetorial descompactado
caminho_arquivo_vetorial = os.path.join(DIRETORIO_TEMPORARIO, ARQUIVO_VETORIAL)

# Carrega o arquivo vetorial com geopandas
try:
    br_municipios = gpd.read_file(caminho_arquivo_vetorial)
except FileNotFoundError:
    print(f"Arquivo {ARQUIVO_VETORIAL} não encontrado no diretório {DIRETORIO_TEMPORARIO}")

# Renomear colunas e transmorda para minúscula
cols_old = br_municipios.columns.to_list()
# lista de novos nomes de colunas
cols_new = [
    'cod_mun', 'nm_mun', 'sigla_uf', 'area_km2']
# Criando um dicionário para mapear nomes antigos para novos
col_mapping = dict(zip(cols_old, cols_new))
# Renomeando as colunas no dataframe
df_mun = br_municipios.rename(columns=col_mapping).reset_index(drop=True)
    
# Corrigindo o tipo de dados INT64 para OBJECT da coluna codmun de ambos datafrane
df_mun['cod6_mun'] = df_mun['cod6_mun'].astype(str)
stats['codmun'] = stats['codmun'].astype(str)

# 
df_mun.insert(0,"cod6_mun", value=df_mun["cod_mun"].astype(str).str.slice(0,6))

# Carregar arquivo contendo as variáveis por município
stats = pd.read_csv('../data/dataset_amostra_stats.csv')



# Mescla os dataframe e preenche com NaN aquelas lingações inexistente
municipios_estudados = df_mun.merge(stats, left_on='cod6_mun', right_on='codmun' )

# Verificando a existência de valores nulos
municipios_estudados[municipios_estudados.isna().any(axis=1)] #não há

# Seelcionando colunas desejadas
gdf = municipios_estudados[[
    'cod6_mun', 'cod_mun', 'nm_mun', 
    'coduf', 'sigla_uf_y', 'nm_uf', 
    'pop2009', 'pop2019', 'nnae_2009', 'nnae_2019',
    'areakm2_municipio', 'areakm2_urbanizada',
    'ii_09', 'ii_19', 'ii_variacao_percentual', 'urbanizacao_percentual',
    'geometry'
]]

gdf.head()

# Plot map
gdf.plot()

# Check SRC
gdf.crs

gdf.to_file('../data/dataset_municipio_stats.geojson', driver='GeoJSON')