import json
import numpy as np
from scipy.spatial import KDTree
from flask import Flask, request, jsonify

app = Flask(__name__)

sorted_bars = []
sorted_coords = []

with open('data/joined_data.json') as joined_data:
    bars = json.load(joined_data)

    for bar in bars:
      sorted_bars.append([bar.get('name'), bar.get('coords'), bar.get('area')])

# sort bars by coordinates for result lookup
sorted(sorted_bars, key=lambda k: [k[1][0], k[1][1]])

# separate list of only coordinates for KDTree
for bar in sorted_bars:
    sorted_coords.append(bar[1])

# KDTree gives us O(log n) lookup for nearest neighbors
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.html
tree = KDTree(np.array(sorted_coords))

@app.route("/nearest_bars/", methods=["POST"])
def nearest_bars():
    req = request.get_json()
    _lat = float(req.get('lat'))
    _long = float(req.get('long'))

    # query kd tree for 5 closest neighbors
    _ , neighbor_indecies = tree.query([_lat, _long], k=5)

    # look up our indecies in our original list to build result
    return jsonify([sorted_bars[idx] for idx in neighbor_indecies])
