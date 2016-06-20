# geospatial-storytelling

Implementation for visualization of personal gps data

## Required packages

- [numpy](http://www.numpy.org/) fundamental package for scientific computing with Python
- [matplotlib](http://matplotlib.org/) python 2D plotting library
- [gdal](https://pypi.python.org/pypi/GDAL) python bindings for Geospatial Data Abstraction Library (and OGR)
- [Basemap](https://github.com/matplotlib/basemap) plot on map projections using matplotlib

## Source files

All the source files in the **src** folder produce images which are saved in the **visualization** folder.

- **simple_scatter.py** 
	Scatter point visualization of the data set over the neighborhoods
- **point_heatmap.py** 
	Heatmap visualization layer 
- **compute_neighborhood_histogram.py**
	This source is necessary to compute the number of points for each neighborhood.
- **neighborhood_heatmap.py**
	Heatmap visualization with histogram bins for each neighborhood. **neighborhood_histogram.npy** is necessary to run this visualization, which is computed by **compute_neighborhood_histogram.py**.

## Data sets

The example data set used for the visualizations was from the [Citibike System Data](https://www.citibikenyc.com/system-data), which can be found on the real-time [Citi Bike station feed](https://feeds.citibikenyc.com/stations/stations.json) GeoJSON file.

The NYC Neighborhood boundaries with the respective are used from the link of the [Pediacities NYC Neighborhoods](http://catalog.opendata.city/dataset/pediacities-nyc-neighborhoods).

![Preview](preview.png)