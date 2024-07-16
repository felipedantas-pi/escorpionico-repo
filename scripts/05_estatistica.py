import pandas as pd

# Lendo dataset amostra
df = pd.read_csv('../data/sinan_datasus/dataset_nnae.csv')

df['cod_mun'] = df['cod_mun'].astype(str)

df.dtypes

# Precisamos calcular:
# - Indice de Incidência 2009
# - Indice de Incidência 2019
# - Variação no periodo
# - Percentual de Urbanização
#
# Calculando íncides de incidencia e variação
df.insert(loc=8, column='ii_09', value=((df["nnae_2009"] / df["pop2009"]) * 10000).round(4))
df.insert(loc=10, column='ii_19', value=((df["nnae_2019"] / df["pop2019"]) * 10000).round(4))
df.insert(
    loc=11, 
    column='ii_variacao_percentual',
    value=(
        ((df["ii_19"] - df["ii_09"]) / df["ii_09"]) * 100).round(2)
    )
# Calculando percentual de área urbanizada
df.insert(
    loc=13, 
    column='urbanizacao_percentual', 
    value=((df["areakm2_urbanizada"] / df["areakm2_municipio"]) * 100).round(4)
    )

## Obter algumas estatísticas descritivas
# 3 Municípios com maiores e menores número absolutos de casos notificados
df.sort_values(by='nnae_2009', axis=0, ascending=False).head(3)
df.sort_values(by='nnae_2009', axis=0, ascending=True).head(3)
df.sort_values(by='nnae_2019', axis=0, ascending=False).head(3)
df.sort_values(by='nnae_2019', axis=0, ascending=True).head(3)

# 3 Municípios com maiores e menores índices de indicência
df.sort_values(by='ii_2009', axis=0, ascending=False).head(3)
df.sort_values(by='ii_2009', axis=0, ascending=True).head(3)
df.sort_values(by='ii_2019', axis=0, ascending=False).head(3)
df.sort_values(by='ii_2019', axis=0, ascending=True).head(3)

# 3 Municípios com menores índices de indicência
df.sort_values(
    by='ii_variacao_percentual', 
    axis=0, ascending=False).head(3)
df.sort_values(
    by='ii_variacao_percentual', 
    axis=0, ascending=True).head(3)

#
df.sort_values(
    by='urbanizacao_percentual', 
    axis=0, ascending=False).head(3)
df.sort_values(
    by='urbanizacao_percentual', 
    axis=0, ascending=True).head(3)

# Valores médios
df.columns.to_list()
df['ii_09'].mean().round(2) #média 2009
df['ii_19'].mean().round(2) # média 2019
df['ii_variacao_percentual'].mean().round(2)
df['urbanizacao_percentual'].mean().round(2)

# Valores médios por estado
df_media = df.groupby('sigla_uf')[['ii_2009','ii_2019','ii_variacao']].mean().reset_index()


df['ii_09'].describe()
df['ii_19'].describe()
df['ii_variacao_percentual'].describe()
df['urbanizacao_percentual'].describe()


# Salvando dataframe
df_media.to_csv('../data/dataset_amostra_stats_media_uf.csv', index=False, encoding='utf-8')
df.to_csv('../data/dataset_amostra_stats.csv', index=False, encoding='utf-8')
