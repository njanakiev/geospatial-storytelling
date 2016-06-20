import os
from mpl_toolkits.basemap.pyproj import Proj
import matplotlib.pyplot as plt
import numpy as np
import json



# Project data to New York Long Island SRS (Spatial Reference System)
# http://www.spatialreference.org/ref/epsg/2263/
p = Proj(init="epsg:2263")

# Load GPS data from url or file
#f = urllib2.urlopen("https://feeds.citibikenyc.com/stations/stations.json")
#jsonData = json.load(f)
with open('../data/citibike.json', 'r') as f:
	jsonData = json.load(f)

X = []
for i in range(len(jsonData['stationBeanList'])):
	lon = jsonData['stationBeanList'][i]['longitude']
	lat = jsonData['stationBeanList'][i]['latitude']
	X.append((lat, lon))
X = np.array(X)
x, y = p(X[:, 1], X[:, 0]) # Projection of coordinates



# Get underlying nyc mapping data
nyc_neighborhoods = "../nyc_data/nyc_neighborhoods.json"
polygons = []
with open(nyc_neighborhoods, 'r') as f:
	jsonData = json.load(f)
	for feature in jsonData['features']:
		for polygon in feature['geometry']['coordinates']:
			polygon = np.array(polygon).squeeze()
			polygon[:,0], polygon[:,1] = p(polygon[:,0], polygon[:,1]) # Projection of coordinates
			polygons.append(polygon)			


heatmap, xedges, yedges = np.histogram2d(y, x, bins=20)
extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]



# Draw visualization
fig, ax = plt.subplots()
fig.set_size_inches(20, 20)
for polygon in polygons:
	ax.plot(polygon[:,0], polygon[:,1], 'k', alpha=0.3)

ax.imshow(heatmap, extent=extent, interpolation='none', cmap=plt.get_cmap('Greys'))
ax.scatter(x, y, marker=".", edgecolors='none', s=5,  c='k', alpha=0.9)

plt.axis('equal')
plt.axis('off')
plt.xlim([extent[0], extent[1]])
plt.ylim([extent[3], extent[2]])
plt.savefig("../visualization/heatmap_visualization.png", bbox_inches='tight', pad_inches=0)