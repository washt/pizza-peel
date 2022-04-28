from functools import partial
import fiona
import pyproj
from shapely.geometry import Point, Polygon
from shapely.ops import transform

all_bars = []

with fiona.open("data/osm-bars/bigquery-public-data-geo-openstreetmap-bars-point.shp") as bars:
  for bar in bars: 
    _id = bar.get('id') 
    coords = bar['geometry']['coordinates']
    name = bar['properties']['name']
    address = bar['properties']['address']
    poi_type = bar['properties']['poi_type']

    all_bars.append([_id, name, poi_type, coords, address])

footprint_polygons = []

with fiona.open("data/ms-bldg-footprints--dc.geojson") as footprints:
  for footprint in footprints: 
    geometry = footprint.get('geometry').get('coordinates')
    footprint_polygons.append(Polygon(geometry[0]))

# Geodetic transform, borrowed from
# https://gist.github.com/robinkraft/c6de2f988c9d3f01af3c
projection = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'),
               pyproj.Proj(init='epsg:3857'))

for bar in all_bars:
  for footprint in footprint_polygons:
    bar_point = Point(bar[3])

    if bar_point.within(footprint):
      transformed = transform(projection, footprint)
      bar.append(transformed.area)
