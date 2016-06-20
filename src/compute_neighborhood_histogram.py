import numpy as np
import matplotlib.pyplot as plt
from osgeo import ogr
import json



# Load GPS data from url or file
#f = urllib2.urlopen("https://feeds.citibikenyc.com/stations/stations.json")
#jsonData = json.load(f)
with open('../data/citibike.json', 'r') as f:
	jsonData = json.load(f)

# Collect GPS points as OGR points
points = []
for i in range(len(jsonData['stationBeanList'])):
	lon = jsonData['stationBeanList'][i]['longitude']
	lat = jsonData['stationBeanList'][i]['latitude']
	
	point = ogr.Geometry(ogr.wkbPoint)
	point.AddPoint(lon, lat)
	points.append(point)

	

# Read in the neighborhoods from geojson file
histogram = {}
shp = ogr.Open("../nyc_data/nyc_neighborhoods.json")
layer = shp.GetLayer(0)
for feature in layer:
	#if feature.GetField("boroughCode") == "1":
	neighborhoodName = feature.GetField("neighborhood")
	histogram[neighborhoodName] = 0
		
	
	geometry = feature.GetGeometryRef()
	if geometry is not None and geometry.GetGeometryType() == ogr.wkbPolygon:
		count = 0
		for point in points:
			count += point.Within(geometry)
			
		histogram[neighborhoodName] = count
		print("%s, count: %i" % (neighborhoodName, count))



# Write neighborhood histogram to npy file
np.save('neighborhood_histogram.npy', histogram)
# Load: d = np.load('neighborhood_histogram.npy').item()

# Write neighborhood histogram to csv file
#f = open("neighborhood_histogram.txt", 'w')
#for key in histogram:
#	f.write("%s;%i\n" % (key, histogram[key]))
#f.close()



# Visualize histogram
keys, values = np.array(histogram.keys()), np.array(histogram.values())

# Mask out all zero values
mask = values != 0
keys, values = keys[mask], values[mask]
# Sort all values
idx = np.argsort(values)
keys, values = keys[idx], values[idx]
pos = np.arange(len(values)) + 0.5

fig, ax = plt.subplots()
fig.set_size_inches(20, 20)
ax.barh(pos, values, color='k')
for i in range(len(keys)):
	ax.text(0, pos[i] + 0.2, keys[i], color='white', fontweight='bold')

plt.ylim([pos[0], pos[-1]+1])
plt.axis('off')
plt.savefig('../visualization/neighborhood_histogram.png', bbox_inches='tight', pad_inches=0)
