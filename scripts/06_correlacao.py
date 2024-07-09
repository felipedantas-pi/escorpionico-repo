import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/dataset_amostra_stats.csv')

df['codmun'] = df['codmun'].astype(str)
df['coduf'] = df['coduf'].astype(str)


# Desenha um gráfico de duas variáveis com gráfico bivariados e univariados
disp09 = sns.jointplot(data=df, x='ii_09', y='urbanizacao_percentual', kind="reg", ci=95)

penguins = sns.load_dataset("penguins")