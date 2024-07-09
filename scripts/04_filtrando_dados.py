import pandas as pd

df = pd.read_csv('../data/dataset_ibge_datasus.csv')

# ordenandos colunas
df = df[['codmun','nm_municipio','coduf','nm_uf','sigla_uf','pop2009','pop2019','nnae_2009','nnae_2019','areakm2_municipio','areakm2_urbanizada']]

df['codmun'] = df['codmun'].astype(str)
df['coduf'] = df['coduf'].astype(str)

# Selecionando os municípios em 2019 >= 60000 habitantes
pop = 60000
df_pop19_60k = df.query('pop2019 >= @pop').reset_index(drop=True).copy()

df_final = df_pop19_60k.sort_values('pop2019', ascending=True).reset_index(drop=True)



df_final.to_csv("../data/dataset_amostra.csv", encoding='utf-8', index=False)

