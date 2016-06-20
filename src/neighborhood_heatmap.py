import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap.pyproj import Proj
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from osgeo import ogr
import json



# Project data to New York Long Island SRS (Spatial Reference System)
# http://www.spatialreference.org/ref/epsg/2263/
p = Proj(init="epsg:2263")

# Load neighborhood histogram
histogram = np.load('neighborhood_histogram.npy').item()

# Load neighborhood polygons into dictionary
neighborhoods = {}
with open("../nyc_data/nyc_neighborhoods.json", 'r') as f:
	jsonData = json.load(f)
	for feature in jsonData['features']:
		polygon = np.array(feature['geometry']['coordinates']).squeeze()
		x, y = p(polygon[:, 0], polygon[:, 1]) # Projection of coordinates
		neighborhoods[feature['properties']['neighborhood']] = np.array(zip(x, y))
	
	

# Create polygon patches
patches = []
colors = []
for key in neighborhoods:
	polygon = Polygon(neighborhoods[key], True)
	patches.append(polygon)
	colors.append(histogram[key])

p = PatchCollection(patches, cmap=plt.get_cmap('gray'))
p.set_array(np.array(colors))



# Visualize patches
fig, ax = plt.subplots()
fig.set_size_inches(20, 20)
ax.add_collection(p)
plt.axis('equal')
plt.axis('off')
plt.savefig('../visualization/neighborhood_heatmap.png', bbox_inches='tight', pad_inches=0)
