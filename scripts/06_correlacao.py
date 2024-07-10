import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('../data/dataset_amostra_stats.csv')

df['codmun'] = df['codmun'].astype(str)
df['coduf'] = df['coduf'].astype(str)

df['ii_variacao_percentual'].min()
df['ii_variacao_percentual'].max()
df["ii_09"].min()
df["ii_09"].max()


################################################
# Histograma
################################################

# Gráfico de distribuição univariada usando a estimativa de densidade de kernel
# Número de bins segundo diferentes regras
n = len(df)
sturges_bins = int(np.ceil(np.log2(n) + 1)) # 1ª regra
rice_bins = int(np.ceil(2 * n**(1/3))) # 2ª regra

# Criando o gráfico Histograma
hist_plot = sns.histplot(data=df, x='ii_variacao_percentual', kde=True, bins=sturges_bins) #opção 2
# Renomear os rótulos dos eixos do histograma
hist_plot.set_xlabel('Percentage Change')
hist_plot.set_ylabel('Density')


#########################################
## Correlação de Spearman
########################################

# Selecionando variáveis
df_2009 = df[["ii_09", "urbanizacao_percentual"]] # Gerará o coeficiente de correlação
df_2019 = df[["ii_19", "urbanizacao_percentual"]] # Gerará o coeficiente de correlação
df_matriz = df[["ii_09", "ii_19", "urbanizacao_percentual"]] # Gerará matriz de correlação

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
rho09, pval09  = spearmanr_pval(df_2009)
rho19, pval19  = spearmanr_pval(df_2019)
rho_df, pval_df  = spearmanr_pval(df_matriz)

#--- Criando o mapa de calor ---#
custom_labels = ['I.I. 2009','I.I.2019','Urbanized Area (%)']

plt.figure(figsize=(10, 10))
h = sns.heatmap(
    data=rho_df, 
    annot=True, 
    cmap='coolwarm',
    vmin=-1, vmax=1)

# Definindo título da figura
plt.title('Mapa de Calor da Matriz de Correlação de Spearman')

h.set(xlabel="", ylabel="", aspect="equal")
h.despine(left=True,Bottom=True)
h.ax.margins(.02)
for label in h.ax.get_xticklabels

# Ajustando os rótulos do eixo X e Y
plt.xticks(ticks=range(len(custom_labels)), labels=custom_labels, ha='left')
plt.yticks(ticks=range(len(custom_labels)), labels=custom_labels)

# Ajusta automaticamente a disposição dos elementos na figura
plt.tight_layout()
plt.show()



###############################################################
# GRAFICO DE DISPERSÃO + HISTOGRA MARGINAL + CORRELAÇÃO
###############################################################

# Gráfico de dispersão + histograma marginal para dados do ii_2009
disp_hist_2009 = sns.jointplot(data=df, x='ii_09', y='urbanizacao_percentual', kind="scatter", height=5, ratio=3 )
disp_hist_2009.set_axis_labels('Incidence Index', 'Percentage Urbanization')
# Adicionar anotação da correlação
plt.annotate(f'Rs: {rho09:.3f}\np-value: {pval09:.3f}', xy=(1, 0.95),
             xycoords='axes fraction', fontsize=7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
#plt.suptitle(' Índice de Incidência x Urbanização Percentual', y=1.02)
#plt.show()


# Gráfico de dispersão + histograma marginal para dados do ii_2009
disp_hist_2019 = sns.jointplot(data=df, x='ii_19', y='urbanizacao_percentual', kind="scatter", height=5, ratio=3 )
disp_hist_2019.set_axis_labels('Incidence Index', 'Percentage Urbanization')
# Adicionar anotação da correlação
plt.annotate(f'Rs: {rho19:.3f}\np-value: {pval19:.3f}', xy=(1, 0.95),
             xycoords='axes fraction', fontsize=7, ha='right', va='top',
             bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white'))
#plt.suptitle(' Índice de Incidência x Urbanização Percentual', y=1.02)
#plt.show()