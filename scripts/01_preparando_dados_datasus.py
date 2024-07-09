#
# Importando bibliotecas
import pandas as pd

# Lendo arquivo CSV baixodo do site TABNET do DATASUS
# arquivo CSV possui algumas informações que não precisaremos.
# ONDE BAIXAR: http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sinannet/cnv/animaisbr.def
dataset = pd.read_csv("../data/sinan_datasus/sinannet_cnv_animaisbr112720189_70_211_56.csv", 
    sep=';', encoding='latin-1', skiprows=4, engine='python', skipfooter=23, na_values=['-'])

# A coluna 'Município de Notificação' é do tipo texto e contém, além do nome do 
# município de notificação, os código destes municípios e a sigla do estado o qual pertencem.
# Criaremos 3 novas colunas a partir da coluna 'Município de Notificação
dataset.insert(0, "codmun", value=dataset["Município de notificação"].str.slice(0,6))
dataset.insert(1, "municipios", value=dataset["Município de notificação"].str.slice(6))
dataset.insert(1, "coduf", value=dataset["Município de notificação"].str.slice(0,2))

# Selecionando apenas as colunas de interesse
dataset = dataset[["codmun", "coduf", "municipios", "2009", "2019"]] # 4646 linhas x 5 colunas

# Um dos critérios do artigo para seleção da amostra é de existir mais de um caso notificado pelo município.
# Então, devemos pesquisa no dataframe por valores NULOS nos dados de notificação de casos
# de acidente com escorpião para o ano de 2009 e 2019
dataset[dataset[['2009','2019']].isna().any(axis=1)] # --> encontrou 2623 linhas

# Agora excluíremos essas linhas, pois um dos critérios de escolha da amostragem é que
# deve existir 1 ou mais casos notificados
# Excluir linhas que têm NaN nas seguintes colunas
df_cleaned = dataset.dropna(subset=['2009', '2019']).reset_index(drop=True).copy()

# Verificando se aindas existe alguma valore NaN em qualquer coluna
df_cleaned[df_cleaned.isna().any(axis=1)]

# Vamos renomear algumas colunas
# Pegando o nome apenas das duas últimas colunas
cols_old = df_cleaned.columns.to_list()[3:]
# lista de novos nomes de colunas
cols_new = ['nnae_2009','nnae_2019']
# Criando um dicionário para mapear nomes antigos para novos
col_mapping = dict(zip(cols_old, cols_new))
# Renomeando as colunas no dataframe
df = df_cleaned.rename(columns=col_mapping).copy()

# Transformar valores do tipo FLOAT para INT das colunas de casos notificados
df['nnae_2009'] = df["nnae_2009"].astype('Int64')
df['nnae_2019'] = df["nnae_2019"].astype('Int64')

# Exportando dataframe para CSV
df.to_csv("../data/sinan_datasus/dataset_nnae.csv", encoding='utf-8', index=False)