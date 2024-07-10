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

# Gráfico de distribuição univariada usando a estimativa de densidade de kernel
# https://seaborn.pydata.org/generated/seaborn.kdeplot.html
sns.kdeplot(data=df, x="ii_variacao_percentual", fill=True) #opção 1
sns.histplot(data=df, x='ii_variacao_percentual', kde=True) #opção 2


# Gráfico de dispersão + histograma marginal para dados do ii_2009
dist2009 = sns.jointplot(data=df, x='ii_09', y='urbanizacao_percentual', kind="scatter", height=5, ratio=3)
dist2009.set_axis_labels('Índice de Incidência', 'Urbanização Percentual')
#plt.suptitle(' Índice de Incidência x Urbanização Percentual', y=1.02)
#plt.show()


# Gráfico de dispersão + histograma marginal para dados do ii_2019
dist2019 = sns.jointplot(data=df, x='ii_19', y='urbanizacao_percentual', kind="scatter", height=5, ratio=3)
dist2019.set_axis_labels('Índice de Incidência', 'Urbanização Percentual')
#plt.suptitle(' Índice de Incidência x Urbanização Percentual', y=1.02)
#plt.show()



