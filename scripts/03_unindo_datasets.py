import pandas as pd

## Leitura dos datasets
df_datasus = pd.read_csv("../data/sinan_datasus/dataset_nnae.csv")
df_ibge = pd.read_csv("../data/ibge/dataset_pop_area_urb.csv")

## Infomações sobre os datasets
df_datasus.info() # Possui 2023 linhas x 5 colunas
df_ibge.info() # Possui 5565 linhas x 8 colunas

# Os dados do dataset do DATASUS, depois da limpeza, contempla apenas os municípios que 
# tiveram casos notificados de acidente com escorpião.
# Precisamos unir os dados do DATASUS ao do IBGE.
df = df_datasus.merge(df_ibge, how='left', on='codmun')

# Deletanado colunas duplicadas
df.drop(columns=['municipios'], inplace=True)

df['codmun'] = df['codmun'].astype(str)
df['coduf'] = df['coduf'].astype(str)

df.to_csv("../data/dataset_ibge_datasus.csv", index=False, encoding='utf-8')
df.to_parquet('../data/dataset_ibge_datasus.parquet', engine='pyarrow', index=False)