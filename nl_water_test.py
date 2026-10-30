"""
maak plaatje van nederland met alleen de bebouwde gebieden
met een cirkel dat totale opp van deze gebieden weergeeft
"""

import pandas as pd
import math
import geopandas as gpd
from shapely.ops import unary_union
import matplotlib.pyplot as plt
from shapely.geometry import Point
from matplotlib.patches import Circle

print('reading grenskaart')
grens=gpd.read_file("bestuurlijkegrenzen.gpkg")
polygons_grens=gpd.GeoSeries(unary_union(grens.geometry))

df2=gpd.read_file("CBS_Publicatiebestand_NBBG2022_v1_def.gpkg")
#filt=[90] #buitenland
#df2=df2[~df2.NBBG22.isin(filt)]
df2=df2[df2.NBBG22<51] #alles niet bebouwd

#polygons=gpd.GeoSeries(unary_union(df2.geometry)) #too slow
areas=[geom.area for geom in df2.geometry]
area=sum(areas)
df2=df2[[a>1e5 for a in areas]]
tolerance=1e2
df2.geometry=df2.geometry.simplify(tolerance)
radius=math.sqrt(area/(2*math.pi))
circle=Point(50000-radius,550000+radius).buffer(radius)

#plot
print('plotting2')
fig, ax = plt.subplots()
fig.set_figheight(15)
fig.set_figwidth(15)
ax.set_facecolor('blue')
polygons_grens.plot(ax=ax,color='blue',edgecolor='black')
pb=df2.plot(ax=ax,color='grey',label='NBBG polygons')
pob=gpd.GeoSeries(circle).plot(ax=ax,color='grey',label=f'total {area = :.3} m2 bebouwd out of 41.5e9 m2')

ax.legend([Circle((0, 0),1,color='grey')],[ax.collections[-1].get_label()],loc=2)

fig.savefig("grote_watersnood2.svg")
plt.show()