from functools import partial
import fiona
import json
import pyproj
from shapely.geometry import Point, Polygon
from shapely.ops import transform

all_bars = []

with fiona.open("data/osm-bars/bigquery-public-data-geo-openstreetmap-bars-point.shp") as bars:
  for bar in bars: 
    name = bar['properties']['name']
    address = bar['properties']['address']
    poi_type = bar['properties']['poi_type']
    coords = bar['geometry']['coordinates']

    all_bars.append({"name": name,"address": address, "poi_type": poi_type, "coords": coords, "area": ""})

footprint_polygons = []

with fiona.open("data/ms-bldg-footprints--dc.geojson") as footprints:
  for footprint in footprints: 
    geometry = footprint.get('geometry').get('coordinates')
    footprint_polygons.append(Polygon(geometry[0]))

# Geodetic transform to calculate area in meters^2
# borrowed from https://gist.github.com/robinkraft/c6de2f988c9d3f01af3c
projection = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),
               pyproj.Proj(init='epsg:3857'))
count = 0
for bar in all_bars:
  for footprint in footprint_polygons:
    bar_point = Point(bar["coords"])

    if bar_point.within(footprint):
      transformed = transform(projection, footprint)
      bar["area"] = transformed.area
      print("Processed", count, "of", len(all_bars))
      count += 1

print("Writing to file..")

with open('data/joined_data.json', 'w') as outfile:
    outfile.write('[')
    for bar in all_bars:
        json.dump(bar, outfile)
        if bar != all_bars[-1]:
            outfile.write(',')
    outfile.write(']')

print('Complete!')