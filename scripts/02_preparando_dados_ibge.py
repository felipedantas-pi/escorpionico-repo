import pandas as pd

######################################################
#####  DATASETS: POPULAÇÃO MUNICIPAL ---------- #####
#######################################################

# Definindo os nomes das colunas
cols_sidraPop = ['codmunicipio','nm_municipio','pop2009','pop2019']
# importando tabela bruta de dados de população por municípios dos anos de 2009 e 2019
# Fonte: https://sidra.ibge.gov.br/Tabela/6579
dfpop = pd.read_excel("../data/ibge/populacao/TabelaSIDRA6579.xlsx",
                      names=cols_sidraPop, skiprows=3, skipfooter=1, na_values=['...'])

# Verificando a existência de valores nulos
dfpop[dfpop[['pop2009','pop2019']].isna().any(axis=1)] # existi 5 linhas vazias em pop2009

# Vamos excluir essas linhas, para compatibilizar a quantidade de municípios
# de 2009 com 2019
dfpop_cleaned = dfpop.dropna(subset=['pop2009']).reset_index(drop=True).copy()

# Desagregando o nome do município da sigla do estado
dfpop_cleaned.insert(1,"municipio", value=dfpop_cleaned["nm_municipio"].str.slice(0,-5))
# O código do município do IBGE possui o padrão de 7 dígitos, porém o código do DATATUS 
# possui 6 dígitos. Precisamos compatibilizar os códigos para futuras operações
dfpop_cleaned.insert(0,"codmun", value=dfpop_cleaned["codmunicipio"].astype(str).str.slice(0,6))
# Desagregando o nome da sigla do estado do nome do município
dfpop_cleaned.insert(3,"siglaUF", value=dfpop_cleaned["nm_municipio"].str.slice(-3,-1))

# Excluíndo coluna antiga
dfpop_cleaned.drop(labels=["codmunicipio", "nm_municipio"], axis=1, inplace=True)

# Transformando o tipo de dados FLOAT para INT
dfpop_cleaned['pop2009'] = dfpop_cleaned['pop2009'].astype('Int64')

# Exportando dataframe para CSV
#dfpop_cleaned.to_csv("../data/ibge/populacao/dataset_populacao.csv", encoding='utf-8', index=False)

################################################
# DATASETS: ÁREA TERRITORIAL 
##################################################

# Definindo URL do dataset IBGE contendo a área territorial por município em 2019
url = "https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/areas_territoriais/2019/AR_BR_RG_UF_RGINT_RGIM_MES_MIC_MUN_2019.xls"
# Lendo dataset área territorial
dfarea = pd.read_excel(url, sheet_name='AR_BR_MUN_2019', decimal=',' , skipfooter=3)

# O código do município do IBGE possui o padrão de 7 dígitos, porém o código do DATATUS 
# possui 6 dígitos. Precisamos compatibilizar os códigos para futuras operações
dfarea.insert(0,"codmun", value=dfarea["CD_GCMUN"].astype(str).str.slice(0,6))

# Deletando colunas desnecessárias
dfarea.drop(labels=["ID","CD_GCUF","NM_UF_SIGLA","CD_GCMUN"], axis=1, inplace=True)

####################################################
# DATASETS: ÁREA URBANIZADA
####################################################

# Definindo nomes de colunas para o dataset de Áreas Urbanizadas por municípios em 2019
nomes_cols = [
    'codigo municipio','nome do municipio',
    'areas urbanizadas densas','area urbanizada pouco densas', 'total de area urbanizada',
    'loteamento vazio','area total mapeada','outro equipamentos urbanos',
    'vazios intraurbanos','vazios remanescentes'
]
# Lendo a planilha contendo os dados de área urbanizada
# Apesar da planilha possui os título da planilha 'MUNICIPIOS_2021' os dados são de 2019
dfurb = pd.read_excel("../data/ibge/urbanizacao/areas_por_recorte_territorial_2019.xlsx",
                      sheet_name='MUNICIPIOS_2021', skiprows=2, skipfooter=1, decimal=',',
                      names=nomes_cols)

# O código do município do IBGE possui o padrão de 7 dígitos, porém o código do DATATUS 
# possui 6 dígitos. Precisamos compatibilizar os códigos para futuras operações
dfurb.insert(0,"codmun", value=dfurb["codigo municipio"].astype(str).str.slice(0,6))

# Selecionandos apenas as colunas de interesse
dfurb_new = dfurb[['codmun', 'nome do municipio', 'total de area urbanizada']]

# Verificando o tamanho das matrizes
dfpop_cleaned.shape # 5565 linhas
dfarea.shape # 5572 linhas
dfurb_new.shape # 5571 linhas

# Vamos unir os 3 datasets e obter um único dataset de dados do IBGE
# O dataset de referências será o de populacao e todos os outros deverão se adequar a ele.
df_pop_area_urb = dfpop_cleaned.merge(dfarea, how='left', on='codmun').merge(dfurb_new, how='left', on='codmun')

# Deletenado colunas desnecessários e duplicadas
df_pop_area_urb.drop(columns=['NM_MUN_2019', 'nome do municipio'], inplace=True)

# Renomeando colunas
cols_old = df_pop_area_urb.columns.to_list()
# lista de novos nomes de colunas
cols_new = [
    'codmun','nm_municipio','sigla_uf',
    'pop2009','pop2019','nm_uf',
    'areakm2_municipio','areakm2_urbanizada']
# Criando um dicionário para mapear nomes antigos para novos
col_mapping = dict(zip(cols_old, cols_new))
# Renomeando as colunas no dataframe
df_all = df_pop_area_urb.rename(columns=col_mapping).reset_index(drop=True)

df_all.to_csv("../data/ibge/dataset_pop_area_urb.csv", encoding="utf-8", index=False)
