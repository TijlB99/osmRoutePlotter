import matplotlib.pyplot as plt
from dotutils.densitymap import *
from dotutils.coords import *
from dotutils.logger import *
from dotutils.color import *
from dotutils.osm import *
from dotutils.io import *
from pathlib import Path
import matplotlib
import os

matplotlib.use('Agg')


NORMAL = r"https://tile.openstreetmap.org/{0}/{1}/{2}.png"
DARK = r"https://cartodb-basemaps-b.global.ssl.fastly.net/dark_all/{0}/{1}/{2}.png"

def plot(inputPath, saveDensityMap=False, savePath="out", zoom=7, dpi=1000, tileServer=DARK, boundingBox=None, verbose=True):
	"""
	kmlPath: path to LocationHistory.kml explorted from Google
	saveDensityMap: save density map
	savePath: folder to save output files into
	Zoom: zoom level for tiles (higher number = closer to surface zoom)
	dpi: dpi of plot (higher = higher dataPointsolution = more detail in dots and lines)
	tileServer: r"https://*.*/{0}/{1}/{2}.png"
	boundingBox: (minLon, maxLon, minLat, maxLat)
	verbose: bool
	"""
	logger = SimpleLogger(verbose)

	Path(savePath).mkdir(parents=True, exist_ok=True)
	if(inputPath.endswith(".json")):
		dataPoints = readJson(inputPath)
	else:
		dataPoints = readKml(inputPath)
	logger.log(f"Input: {dataPoints.shape[0]} points.")
	dataPoints = removeCloseAndFarPoints(dataPoints, 1e-3, 15)
	logger.log(f"Reduced to {dataPoints.shape[0]} points.")
	
	if boundingBox is not None:
		(minx, maxx, miny, maxy) = boundingBox
	else:
		minx, maxx, miny, maxy = getBounds(dataPoints)
	
	logger.log(f"Bounding box: lat: {miny} -> {maxy}, lon: {minx} -> {maxx}.")

	densityMap = DensityMap(dataPoints, 100, rescaleFunction=np.sqrt)

	if saveDensityMap:
		dMapPath = os.path.join(savePath, "map.png")
		logger.log(f"Saving density map to {dMapPath}.")
		densityMap.draw(dMapPath)

	_plotByGrouping(dataPoints, densityMap, zoom)
	
	a, bbox = getImageCluster(minx, maxx, miny, maxy, zoom, tileServer)
	plt.imshow(np.asarray(a), zorder=0, extent = bbox, aspect= 'equal')
	
	if boundingBox is None:
		plt.xlim(bbox[0], bbox[1])	
		plt.ylim(bbox[2], bbox[3])
	else:
		plt.xlim(lon2num(minx, zoom), lon2num(maxx, zoom))	
		plt.ylim(lat2num(miny, zoom), lat2num(maxy, zoom))

	plotPath = os.path.join(savePath, "plot.png")
	logger.log(f"Saving fig to {plotPath}")

	plt.axis('off')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.gca().xaxis.set_major_locator(plt.NullLocator())
	plt.gca().yaxis.set_major_locator(plt.NullLocator())
	plt.savefig(plotPath, bbox_inches=0, dpi=dpi, transparent=True)
	logger.log("done!")	

def _plotByGrouping(dataPoints, densityMap, zoom, plt=plt):
	"""
	Connects dots close to each other in time and distance relative to density map
	"""
	groups = groupByDate(dataPoints, 7)
	for group in groups:
		color = generatePastelColor()
		rs = splitOnDist(groups[group], 1, densityMap)
		for r in rs:
			plt.plot(lons2nums(r[:,0].astype(float), zoom), lats2nums(r[:,1].astype(float), zoom),".", color=color, markersize=0.5, mew=0, linewidth=0.1, linestyle="-")


if __name__ == "__main__":
	plot("/path/to/LocationHistory.kml", verbose=True)
