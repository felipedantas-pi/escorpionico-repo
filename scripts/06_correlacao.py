import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('../data/dataset_amostra_stats.csv')

df.dtypes

df['cod_mun'] = df['cod_mun'].astype(str)
df['sigla_uf'] = df['sigla_uf'].astype(str)

df['ii_variacao'].min()
df['ii_variacao'].max()
df["ii_2009"].min()
df["ii_2009"].max()


################################################
# Histograma
################################################

# Gráfico de distribuição univariada usando a estimativa de densidade de kernel
# Número de bins segundo diferentes regras
n = len(df)
sturges_bins = int(np.ceil(np.log2(n) + 1)) # 1ª regra
rice_bins = int(np.ceil(2 * n**(1/3))) # 2ª regra

# Criando o gráfico Histograma
hist_plot = sns.histplot(data=df, x='ii_variacao', kde=True, bins=sturges_bins) #opção 2
# Renomear os rótulos dos eixos do histograma
hist_plot.set_xlabel('% Change', )
hist_plot.set_ylabel('Density')
hist_plot.set_title("Histogram of the Percentage of Variation", pad= 10)


#########################################
## Correlação de Spearman
########################################

# Selecionando variáveis
df_ii_2009 = df[["ii_2009", "percentual_urbanizacao"]] # Gerará o coeficiente de correlação
df_ii_2019 = df[["ii_2019", "percentual_urbanizacao"]] # Gerará o coeficiente de correlação
df_var_2019 = df[["ii_variacao", "percentual_urbanizacao"]] # Gerará o coeficiente de correlação
df_matriz = df[["ii_2009", "ii_2019", 'ii_variacao', "percentual_urbanizacao"]] # Gerará matriz de correlação

# Scipy= Calcula coeficiente de correlação de Spearman com p-value associado
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
# docs:
# O coeficiente de correlação de ordem de classificação de Spearman é uma medida 
# não paramétrica da monotonicidade da relação entre dois conjuntos de dados. 
# Como outros coeficientes de correlação, esse varia entre -1 e +1, com 0 implicando em nenhuma 
# correlação. 
# As correlações de -1 ou +1 implicam uma relação monotônica exata. 
# Correlações positivas implicam que, à medida que x aumenta, y também aumenta. 
# Correlações negativas implicam que, à medida que x aumenta, y diminui.

def spearmanr_pval(df):
    """
    Calcula coeficiente de correlação de Spearman com p-value associado para um DataFrame.
    
    Parâmetros:
    df (DataFrame): DataFrame contendo os dados para calcular a correlação de Spearman.
    
    Retorna:
    rho (DataFrame): Matriz de correlação de Spearman entre as variáveis.
    pval (DataFrame): Matriz de p-values associados às correlações de Spearman.
    """
    rho, pval = stats.spearmanr(df)
    
    if df.shape[1] > 2:
        print("Retornando Matriz de Correlação")
        rho = pd.DataFrame(rho, index=df.columns, columns=df.columns)
        pval = pd.DataFrame(pval, index=df.columns, columns=df.columns)
        return rho, pval
        
    print(f"Retornando o coeficiente de correlação.")
    return rho, pval

# Calcula a matriz/coeficiente de correlação de spearman e os p-valores
rho09, pval09  = spearmanr_pval(df_ii_2009)
rho19, pval19  = spearmanr_pval(df_ii_2019)
rhoVar, pvalVar  = spearmanr_pval(df_var_2019)
rho_df, pval_df  = spearmanr_pval(df_matriz)


###############################################################
# GRAFICO DE DISPERSÃO + HISTOGRA MARGINAL + CORRELAÇÃO
###############################################################

# Gráfico de dispersão + histograma marginal para dados do ii_2009
disp_hist_2009 = sns.jointplot(data=df, x='percentual_urbanizacao', y='ii_2009', kind="scatter", height=5, ratio=3 )
disp_hist_2009.set_axis_labels('Urbanized area (%)','Incidence in 2009 per 10000 inhabitants')
# Adicionar anotação da correlação
plt.annotate(f'Rs: {rho09:.3f}\np-value: {pval09:.3f}', xy=(1, 0.95),
             xycoords='axes fraction', fontsize=7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
#plt.title('Spearman correlation 2009', y=1.4)
plt.title('Correlation between scorpion sting incidence and urbanized area 2009', x=0.5, y=1.4)
#plt.show()


# Gráfico de dispersão + histograma marginal para dados do ii_2019
disp_hist_2019 = sns.jointplot(data=df, x='percentual_urbanizacao', y='ii_2019', kind="scatter", height=5, ratio=3 )
disp_hist_2019.set_axis_labels('Urbanized area (%)','Incidence in 2019 per 10000 inhabitants')
# Adicionar anotação da correlação
plt.annotate(f'Rs: {rho19:.3f}\np-value: {pval19:.3f}', xy=(1, 0.95),
             xycoords='axes fraction', fontsize=7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
#plt.title('Spearman correlation 2019', y=1.4)
plt.title('Correlation between scorpion sting incidence and urbanized area 2019', x=0.5, y=1.4)
#plt.show()


# Gráfico de dispersão + histograma marginal para dados do variacao dos indices
disp_hist_var = sns.jointplot(data=df, x='percentual_urbanizacao', y='ii_variacao', kind="scatter", height=5, ratio=3 )
disp_hist_var.set_axis_labels('Urbanized area (%)','Change in incidents (%)')
# Adicionar anotação da correlação
plt.annotate(f'Rs: {rhoVar:.3f}\np-value: {pvalVar:.3f}', xy=(1, 0.95),
             xycoords='axes fraction', fontsize=7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
#plt.title('Spearman correlation 2019', y=1.4)
plt.title('Correlation between the variation in the incidence\nof scorpion stings and the urbanized area', x=0.5, y=1.4)
#plt.show()

############################################################
# Mapa de calor da matriz de correlação
############################################################

custom_labels = ['I.I. 2009','I.I.2019','Variation (%)', 'Urbanized Area (%)']

plt.figure(figsize=(10, 10))
h = sns.heatmap(
    data=rho_df, 
    annot=True, 
    cmap='coolwarm',
    vmin=-1, vmax=1)

# Definindo título da figura
plt.title('Mapa de Calor da Matriz de Correlação de Spearman')

# Ajustando os rótulos do eixo X e Y
h.set_xticklabels(custom_labels, rotation=45, ha='right')
h.set_yticklabels(custom_labels, rotation=45)

# Ajusta automaticamente a disposição dos elementos na figura
plt.tight_layout()

# Mostrar o gráfico
plt.show()