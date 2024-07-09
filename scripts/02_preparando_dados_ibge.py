import pandas as pd

# Definindo os nomes das colunas
cols_sidraPop = ['codmunicipio','nm_municipio','pop2009','pop2019']
# importando tabela bruta de dados de população por municípios dos anos de 2009 e 2019
dfpop = pd.read_excel("../data/ibge/populacao/TabelaSIDRA6579.xlsx",
                      names=cols_sidraPop, skiprows=3, skipfooter=1, na_values=['...'])

# Verificando a existência de valores nulos
dfpop[dfpop[['pop2009','pop2019']].isna().any(axis=1)] # existi 5 linhas vazias em pop2009

# Vamos excluir essas linhas, para compatibilizar a quantidade de municípios
# de 2009 com 2019
dfcleaned = dfpop.dropna(subset=['pop2009']).reset_index(drop=True).copy()

# Desagregando o nome do município da sigla do estado
dfcleaned.insert(1,"municipio", value=dfcleaned["nm_municipio"].str.slice(0,-5))
# O código do município do IBGE possui o padrão de 7 dígitos, porém o código do DATATUS 
# possui 6 dígitos. Precisamos compatibilizar os códigos para futuras operações
dfcleaned.insert(0,"codmun", value=dfcleaned["codmunicipio"].astype(str).str.slice(0,6))
# Desagregando o nome da sigla do estado do nome do município
dfcleaned.insert(3,"siglaUF", value=dfcleaned["nm_municipio"].str.slice(-3,-1))

# Excluíndo coluna antiga
dfcleaned.drop(labels=["codmunicipio", "nm_municipio"], axis=1, inplace=True)

# Transformando o tipo de dados FLOAT para INT
dfcleaned['pop2009'] = dfcleaned['pop2009'].astype('Int64')

# Exportando dataframe para CSV
dfcleaned.to_csv("../data/ibge/populacao/dataset_populacao.csv", encoding='utf-8', index=False)
