import pandas as pd

## Leitura dos datasets
df_datasus = pd.read_csv("../data/sinan_datasus/dataset_nnae.csv")
df_ibge = pd.read_csv("../data/ibge/dataset_pop_area_urb.csv")

# Verificar se o df-datasus é um subconjunto de df_ibge
set(df_datasus['nm_municipio'].to_list()).issubset(set(df_ibge['nm_municipio'].to_list()))
# Caso não seja, mostra qual valores não fazem parte, utilizando a diferença entre conjuntos
set(df_datasus['nm_municipio'].to_list()) - (set(df_ibge['nm_municipio'].to_list()))

## Infomações sobre os datasets
#df_datasus.info() # Possui 2023 linhas x 5 colunas
df_ibge.info() # Possui 5565 linhas x 8 colunas

# Os dados do dataset do DATASUS, depois da limpeza, contempla apenas os municípios que 
# tiveram casos notificados de acidente com escorpião.
# Precisamos unir os dados do DATASUS ao do IBGE.
df = df_datasus.merge(df_ibge, how='left', left_on='cod_mun', right_on='codmun')

# Identificando as duplicatas na coluna 'municipio'
duplicated_mask = df['cod_mun'].duplicated(keep=False)
# Filtrando as linhas duplicadas
duplicated_values = df.loc[duplicated_mask]

df_unique = df.drop_duplicates(subset=['cod_mun'])

# Deletanado colunas duplicadas
df_unique.drop(columns=['municipio','estado'], inplace=True)

df.dtypes

df_unique['codmun'] = df_unique['codmun'].astype(str)
df_unique['sigla_uf'] = df_unique['sigla_uf'].astype(str)

df_unique.to_csv("../data/dataset_ibge_datasus.csv", index=False, encoding='utf-8')
df_unique.to_parquet('../data/dataset_ibge_datasus.parquet', engine='pyarrow', index=False)