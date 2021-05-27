import pandas as pd
import folium
import random



df=pd.read_csv('Volcanoes.csv')
vmap=folium.Map(location=[46.869801, -121.751000],zoom_start=5)
lat=list(df['LAT'])
lon=list(df['LON'])
name=list(df['NAME'])
height=list(df['ELEV'])
status=list(df['STATUS'])

html = """<h4>Volcano information:</h4>
Name: %s <br>
Height: %s <br>
Status: %s 
"""

# This is for random coloring the markers
# colorList=['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple','pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
# def randomColorPicker():
#     return random.choice(colorList)

# This is for coloring marker Green,Orange,Red based on their elevation
def elevationColor(ht):
    if ht<=1000:
        return 'green'
    elif ht<=3000:
        return 'orange'
    else:
        return 'red'

vmLayer=folium.FeatureGroup(name='Volcano Marker Layer')
pmLayer=folium.FeatureGroup(name='Population Heatmap Layer')

for la,ln,nm,ht,st in zip(lat,lon,name,height,status):
    iframe = folium.IFrame(html=html %  (nm,str(ht),st), width=200, height=100)
    vmLayer.add_child(folium.CircleMarker(location=[la,ln],popup=folium.Popup(iframe),radius=6,fill_color=elevationColor(ht),color='grey',fill_opacity=0.7))

pmLayer.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
                    style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000
                                            else 'green' if x['properties']['POP2005']<50000000
                                                         else 'orange' if x['properties']['POP2005']<100000000
                                                                        else 'red'}))

vmap.add_child(vmLayer)
vmap.add_child(pmLayer)
vmap.add_child(folium.LayerControl())
vmap.save('VolcanoMap.html')