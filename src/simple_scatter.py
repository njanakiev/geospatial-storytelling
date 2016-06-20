import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap.pyproj import Proj
from osgeo import ogr
import json
import urllib2



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



# Get underlying nyc mapping data (can be done both with json or ogr library)
polygons = []
with open("../nyc_data/nyc_neighborhoods.json", 'r') as f:
	jsonData = json.load(f)
	for feature in jsonData['features']:
		for polygon in feature['geometry']['coordinates']:
			polygon = np.array(polygon).squeeze()
			polygon[:,0], polygon[:,1] = p(polygon[:,0], polygon[:,1]) # Projection of coordinates
			polygons.append(polygon)



# Draw Visualization
fig, ax = plt.subplots()
fig.set_size_inches(20, 20)
for polygon in polygons:
	plt.plot(polygon[:,0], polygon[:,1], 'k', alpha=0.3)

plt.scatter(x, y, edgecolor='', facecolor='k')
plt.axis('equal')
plt.axis('off')
plt.savefig('../visualization/simple_scatter.png', bbox_inches='tight', pad_inches=0)
