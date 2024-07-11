# Geodados
import geopandas as gpd

# plotting
import matplotlib.pyplot as plt
import mapclassify
import libpysal

# Paleta de cores
from pypalettes import load_cmap

# Anotações
from matplotlib.font_manager import FontProperties
#from matplotlib.patches import FancyArrowPatch
#from highlight_text import fig_text, ax_text

br_uf = gpd.read_file('../data/ibge/malha_territorial/BR_UF_2019.shp')
br_mun = gpd.read_file('../data/ibge/malha_territorial/BR_Municipios_2019.shp')
gdf = gpd.read_file("../data/dataset_municipio_stats.geojson")

gdf.head(3)
gdf.shape
gdf.dtypes
gdf.plot()

# Load the fonts
personal_path = '../fontes/' 
font = FontProperties(fname=personal_path + 'NotoSans-Regular.ttf')
other_font_light = FontProperties(fname=personal_path + 'NotoSans-Light.ttf')
other_medium_font = FontProperties(fname=personal_path + 'NotoSans-Medium.ttf')
other_bold_font = FontProperties(fname=personal_path + 'NotoSans-Bold.ttf')

################################################
### Mapa comparativo dos ìndices de incidência
################################################

def replace_legend_items(legend, mapping):
    """
    Substitui os itens da legenda por valores mapeados específicos.

    Esta função percorre os textos da legenda de um gráfico e substitui cada item
    de acordo com um mapeamento fornecido. É útil quando você precisa alterar as
    descrições automáticas de classes em um mapa coroplético para algo mais legível.

    Parâmetros:
    -----------
    legend : matplotlib.legend.Legend
        A legenda do gráfico que será modificada. Normalmente obtida a partir do método `get_legend()`
        de um objeto de eixo (ax).

    mapping : dict
        Um dicionário onde as chaves são os valores originais da legenda e os valores são as novas
        descrições que devem substituir as originais.

    Exemplo de uso:
    ---------------
    >>> legend = ax.get_legend()
    >>> mapping = {0: 'Muito Baixo', 1: 'Baixo', 2: 'Médio', 3: 'Alto', 4: 'Muito Alto'}
    >>> replace_legend_items(legend, mapping)
    """
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)

# Carrega colormap e outras cores
cmap_ii = load_cmap('gley', type='continuous', reverse=False)
background_color = 'white'
text_color = 'black'

# Classificação Jenks
nb5_2009 = mapclassify.NaturalBreaks(gdf['ii_09'], k=5)
nb5_2019 = mapclassify.NaturalBreaks(gdf['ii_19'], k=5)

# Mapa Coroplético
mapping_2009 = dict([(i, s) for i, s in enumerate(nb5_2009.get_legend_classes())])
mapping_2019 = dict([(i, s) for i, s in enumerate(nb5_2019.get_legend_classes())])

# initialize the figure
fig, axes = plt.subplots(1, 2, figsize=(16, 9), dpi=600)
fig.suptitle('Incidence rate per 10000 inhabitants',
             fontproperties=other_bold_font,
             color=text_color,
             y=0.85
    )
fig.set_facecolor(background_color)

for ax in axes:
    ax.set_facecolor(background_color)

# Criando primeiro gráfico
br_uf.boundary.plot(
    ax=axes[0],
    color='black',
    linewidth=0.6,
)

# informação complementar 2009
gdf.assign(ii09_nb=nb5_2009.yb).plot(
    ax=axes[0],
    column='ii09_nb',
    cmap=cmap_ii,
    edgecolor='black',
    categorical=True,
    linewidth=0.5,
    legend=True,
    legend_kwds={
        "fmt": "{:.2f}",
        "loc": "lower left",
        "bbox_to_anchor": (0., 0., 0.5, 0.5),
        "prop": font,
    }
)

axes[0].set_xlim(-75, -32)
axes[0].set_ylim(-34, 6)
axes[0].set_axis_off()
axes[0].set_title('2009', fontproperties=other_medium_font, color=text_color)

# Ajuste a legenda do segundo gráfico
legend1 = axes[0].get_legend()
legend1.get_frame().set_visible(False)
replace_legend_items(legend1, mapping_2009)

# Criando segundo gráfico (exemplo com dados diferentes)
br_uf.boundary.plot(
    ax=axes[1],
    color='black',
    linewidth=0.6,
)

gdf.assign(ii19_nb=nb5_2019.yb).plot(
    ax=axes[1],
    column='ii19_nb',
    cmap=cmap_ii,
    edgecolor='black',
    categorical=True,
    linewidth=0.5,
    legend=True,
    legend_kwds={
        "fmt": "{:.2f}",
        "loc": "lower left",
        "bbox_to_anchor": (0., 0., 0.5, 0.5),
        "prop": font,
        "frameon":False
    }
)

axes[1].set_xlim(-75, -32)
axes[1].set_ylim(-34, 6)
axes[1].set_axis_off()
axes[1].set_title('2019', fontproperties=other_medium_font, color=text_color)  # Exemplo, substitua pelos dados reais

# Ajuste a legenda do segundo gráfico
legend2 = axes[1].get_legend()
legend2.get_frame().set_visible(False)
replace_legend_items(legend2, mapping_2019)

# Mostrar o mapa
plt.show()

#######################################
############### Variação PERCENTUAL
#######################################

# Classificação Jenks
nb5_iivp = mapclassify.PrettyBreaks(gdf['ii_variacao_percentual'], k=10)

# Mapeando classes da legenda
mapping_v = dict([(i, s) for i, s in enumerate(nb5_iivp.get_legend_classes())])
                
# Carrega colormap e outras cores
#cmap_v = load_cmap('Bay', type='continuous', reverse=True)
cmap_v = load_cmap('RdYlBu_r', type='continuous')
background_color = 'white'
text_color = 'black'

# initialize the figure
fig, ax = plt.subplots(figsize=(16, 9), dpi=600)
fig.suptitle('Change in indices (%)',
             fontsize=14.,
             fontweight='bold',
             fontproperties=other_bold_font,
             color=text_color,
             y=0.92)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

# Criando segundo gráfico (exemplo com dados diferentes)
br_uf.boundary.plot(
    ax=ax,
    color='black',
    linewidth=0.6,
)

# create the plot
gdf.assign(ii_v=nb5_iivp.yb).plot(
    ax=ax,
    figsize=(16,9),
    column='ii_v',
    categorical=True,
    cmap=cmap_v,
    edgecolor='black',
    linewidth=0.5,
    legend=True,
    legend_kwds={
        "fmt": "{:.2f}",
        "loc": "lower left",
        "bbox_to_anchor": (0., 0., 0.5, 0.5),
        "prop": font,
        "frameon": False
    },
)

# custom axis
ax.set_xlim(-75, -32)
ax.set_ylim(-34, 6)
# Desabilida a moldura
ax.set_axis_off()

# Ajuste a legenda do segundo gráfico
legend = ax.get_legend()
replace_legend_items(legend, mapping_v)
    
# Mostrar o mapa
plt.show()