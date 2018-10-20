import folium
import pandas

# function to choose color based on elevation
def color_selection(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# creating a map trough folium
map = folium.Map(location = [37.285554, -121.876516], zoom_start=6, tiles='Mapbox Bright')

# creating a feature group object to put volcanoes markers in it and handle them as a single layer.
map_fgv = folium.FeatureGroup(name = "Volcanoes")

# using pandas to iterate over Volcanoes.txt to get all locations (LAT,LON) and name (NAME) of Volcanoes
data = pandas.read_csv("Volcanoes.txt")
df = data[['LAT','LON','NAME','ELEV']]

for index, row in df.iterrows():
    location = [row['LAT'],row['LON']]
    name_elev = row['NAME'] + ', ' + str(row['ELEV']) + "m"
    color = color_selection(row['ELEV'])
    # adding a child to map_fg object which sets a marker at San Jose
    map_fgv.add_child(folium.CircleMarker(location=location, radius=5, color=color, fill_color=color, fill_opacity=0.9, popup=folium.Popup(name_elev)))

# creating a feature group object to put populations in it and handle them as a single layer.
map_fgp = folium.FeatureGroup(name="Population")

# adding a GeoJSON layer to the map
map_fgp.add_child(folium.GeoJson(data=open('world.json', 'r').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# adding map_fgv to map object
map.add_child(map_fgv)
# adding map_fgv to map object
map.add_child(map_fgp)
# adding a LayerControl to the map for a clear seperation of marker and population layer
map.add_child(folium.LayerControl(position='topright', collapsed=True, autoZIndex=True))

# saving the map object in HTML page
map.save("webmap.html")
