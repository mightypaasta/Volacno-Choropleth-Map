import pandas as pd
import folium
import random


# Storing the dataset of volcano in var df
df=pd.read_csv('Volcanoes.csv')

# Creating map object with folium in vmap(VolcanoMap)
vmap=folium.Map(location=[46.869801, -121.751000],zoom_start=5)

# Storing the latitude , longitude , name of the volcano , height of the volcano , status of the volcano
lat=list(df['LAT'])
lon=list(df['LON'])
name=list(df['NAME'])
height=list(df['ELEV'])
status=list(df['STATUS'])

# Following line will add html funcionality when clicked over the volcano marker, giving more information about volcanoes
html = """<h4>Volcano information:</h4>
Name: %s <br>
Height: %s <br>
Status: %s 
"""

# This is for random coloring the markers
# colorList=['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
# def randomColorPicker():
#     return random.choice(colorList)

# This is for coloring marker Green,Orange,Red based on the elevation of volcanoes
def elevationColor(ht):
    if ht<=1000:
        return 'green'
    elif ht<=3000:
        return 'orange'
    else:
        return 'red'

# Creating separate layer for Volcanoes Marker(vmLayer) and Population Heatmap(pmLayer)
# vmLayer stores all the marker for the volcanos
vmLayer=folium.FeatureGroup(name='Volcano Marker Layer')
# pmLayer stores the population heatmap of the world
pmLayer=folium.FeatureGroup(name='Population Heatmap Layer')

# Following loop will mark all the location of the volcanoes on the map and coloring the marker based on their height
for la,ln,nm,ht,st in zip(lat,lon,name,height,status):
    iframe = folium.IFrame(html=html %  (nm,str(ht),st), width=200, height=100)
    vmLayer.add_child(folium.CircleMarker(location=[la,ln],popup=folium.Popup(iframe),radius=6,fill_color=elevationColor(ht),color='grey',fill_opacity=0.7))

# Following function will color the country on the map based on their population thus creating heatmap of the population
pmLayer.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000
                                            else 'green' if x['properties']['POP2005']<50000000
                                                         else 'orange' if x['properties']['POP2005']<100000000
                                                                        else 'red'}))

# Adding vmLayer and pmLayer in the map in order to work
vmap.add_child(vmLayer)
vmap.add_child(pmLayer)

# LayerControl will allow to turn on/off the layer at the top right of the map. Giving more control to the user
vmap.add_child(folium.LayerControl())
vmap.save('VolcanoMap.html')