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
from matplotlib.patches import FancyArrowPatch
from highlight_text import fig_text, ax_text

gdf = gpd.read_file("../data/dataset_final.geojson")
gdf.head(3)
gdf.shape
gdf.dtypes


gdf["ii_09"].min()
gdf["ii_09"].max()

gdf["ii_19"].min()
gdf["ii_19"].max()

#######################################
############### II 2009
#######################################

# Classificação Jenks
nb5_2009 = mapclassify.NaturalBreaks(gdf['ii_09'], k=5)

# Mapa Coroplético
mapping = dict([(i, s) for i, s in enumerate(nb5_2009.get_legend_classes())])

def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)
                
                
# Carrega colormap e outras cores
cmap = load_cmap('gley', type='continuous', reverse=False)
background_color = 'white'
text_color = 'black'

# Load the fonts
personal_path = '../fontes/' 
font = FontProperties(fname=personal_path + 'BebasNeue-Regular.ttf')
other_font = FontProperties(fname=personal_path + 'FiraSans-Light.ttf')
other_bold_font = FontProperties(fname=personal_path + 'FiraSans-Medium.ttf')

# initialize the figure
fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

# create the plot
gdf.assign(ii09_nb=nb5_2009.yb).plot(
    ax=ax,
    figsize=(16,9),
    column='ii09_nb',
    categorical=True,
    k=5,
    cmap=cmap,
    edgecolor='black',
    linewidth=0.5,
    legend=True,
    legend_kwds={"loc": "lower left"},
)

# custom axis
ax.set_xlim(-75, -32)
ax.set_ylim(-34, 6)
# Desabilida a moldura
ax.set_axis_off()

#
replace_legend_items(ax.get_legend(), mapping)

# Adicionar rótulos aos dados geográficos
for idx, row in gdf.iterrows():
    # Calcula o centroide do polígono
    centroid = row['geometry'].centroid
    # Anotar o rótulo no centroide
    ax.annotate(text=row['SIGLA_UF'], xy=(centroid.x, centroid.y),
                horizontalalignment='center', fontsize=8, color='black')
    
# Mostrar o mapa
plt.show()



#######################################
############### II 2019
#######################################

# Classificação Jenks
nb5_2019 = mapclassify.NaturalBreaks(gdf['ii_19'], k=5)

# Mapa Coroplético
mapping = dict([(i, s) for i, s in enumerate(nb5_2019.get_legend_classes())])

def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)
                
                
# Carrega colormap e outras cores
cmap = load_cmap('gley', type='continuous', reverse=False)
background_color = 'white'
text_color = 'black'

# Load the fonts
personal_path = '../fontes/' 
font = FontProperties(fname=personal_path + 'BebasNeue-Regular.ttf')
other_font = FontProperties(fname=personal_path + 'FiraSans-Light.ttf')
other_bold_font = FontProperties(fname=personal_path + 'FiraSans-Medium.ttf')

# initialize the figure
fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

# create the plot
gdf.assign(ii19_nb=nb5_2019.yb).plot(
    ax=ax,
    figsize=(16,9),
    column='ii19_nb',
    categorical=True,
    k=5,
    cmap=cmap,
    edgecolor='black',
    linewidth=0.5,
    legend=True,
    legend_kwds={"loc": "lower left"},
)

# custom axis
ax.set_xlim(-75, -32)
ax.set_ylim(-34, 6)
# Desabilida a moldura
ax.set_axis_off()

#
replace_legend_items(ax.get_legend(), mapping)

# Adicionar rótulos aos dados geográficos
for idx, row in gdf.iterrows():
    # Calcula o centroide do polígono
    centroid = row['geometry'].centroid
    # Anotar o rótulo no centroide
    ax.annotate(text=row['SIGLA_UF'], xy=(centroid.x, centroid.y),
                horizontalalignment='center', fontsize=8, color='black')
    
# Mostrar o mapa
plt.show()

#######################################
############### Variação PERCENTUAL
#######################################

# Classificação Jenks
nb5_iivp = mapclassify.NaturalBreaks(gdf['ii_variacao_percentual'], k=5)

# Mapa Coroplético
mapping = dict([(i, s) for i, s in enumerate(nb5_iivp.get_legend_classes())])

def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        for k, v in mapping.items():
            if txt.get_text() == str(k):
                txt.set_text(v)
                
                
# Carrega colormap e outras cores
cmap = load_cmap('Tangerines', type='continuous', reverse=True)
background_color = 'white'
text_color = 'black'

# Load the fonts
personal_path = '../fontes/' 
font = FontProperties(fname=personal_path + 'BebasNeue-Regular.ttf')
other_font = FontProperties(fname=personal_path + 'FiraSans-Light.ttf')
other_bold_font = FontProperties(fname=personal_path + 'FiraSans-Medium.ttf')

# initialize the figure
fig, ax = plt.subplots(figsize=(15, 8), dpi=300)
fig.set_facecolor(background_color)
ax.set_facecolor(background_color)

# create the plot
gdf.assign(ii19_nb=nb5_iivp.yb).plot(
    ax=ax,
    figsize=(16,9),
    column='ii19_nb',
    categorical=True,
    k=5,
    cmap=cmap,
    edgecolor='black',
    linewidth=0.5,
    legend=True,
    legend_kwds={"loc": "lower left"},
)

# custom axis
ax.set_xlim(-75, -32)
ax.set_ylim(-34, 6)
# Desabilida a moldura
ax.set_axis_off()

#
replace_legend_items(ax.get_legend(), mapping)

# Adicionar rótulos aos dados geográficos
for idx, row in gdf.iterrows():
    # Calcula o centroide do polígono
    centroid = row['geometry'].centroid
    # Anotar o rótulo no centroide
    ax.annotate(text=row['SIGLA_UF'], xy=(centroid.x, centroid.y),
                horizontalalignment='center', fontsize=8, color='black')
    
# Mostrar o mapa
plt.show()