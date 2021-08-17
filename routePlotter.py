import matplotlib.pyplot as plt
from dotutils.densitymap import *
from dotutils.coords import *
from dotutils.color import *
from dotutils.osm import *
from dotutils.io import *
from pathlib import Path
import matplotlib
import os

matplotlib.use('Agg')


NORMAL = r"https://tile.openstreetmap.org/{0}/{1}/{2}.png"
DARK = r"https://cartodb-basemaps-b.global.ssl.fastly.net/dark_all/{0}/{1}/{2}.png"

def plot(kmlPath, saveMap=True, savePath="out", zoom=7, dpi=1000, tileServer=DARK):
	Path(savePath).mkdir(parents=True, exist_ok=True)
	res = readKml(kmlPath)
	print(f"Input: {res.shape[0]} points.")
	res = removeClosePoints(res, 1e-3, 15)
	print(f"Reduced to {res.shape[0]} points.")
	
	minx, maxx, miny, maxy = getBounds(res)

	dMap, opt = makeDensityMap(res, 100)
	dMap = np.sqrt(dMap)
	drawDMap(dMap, os.path.join(savePath, "map.png"))

	groups = groupByDate(res, 7)
	for group in groups:
		pastel_factor = 0.5
		color = generatePastelColor()
		rs = splitOnDist(groups[group], 1, dMap, opt)
		for r in rs:
			plt.plot(lons2nums(r[:,0].astype(float), zoom), lats2nums(r[:,1].astype(float), zoom),".", color=color, markersize=0.5, mew=0, linewidth=0.1, linestyle="-")

	
	a, bbox = getImageCluster(minx, maxx, miny, maxy, zoom, tileServer)
	plt.imshow(np.asarray(a), zorder=0, extent = bbox, aspect= 'equal')
	
	plt.xlim(bbox[0], bbox[1])	
	plt.ylim(bbox[2], bbox[3])
	
	print("Saving fig")
	plt.axis('off')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.gca().xaxis.set_major_locator(plt.NullLocator())
	plt.gca().yaxis.set_major_locator(plt.NullLocator())
	plt.savefig(os.path.join(savePath, "plot.png"), bbox_inches=0, dpi=dpi, transparent=True)
	print("done!")	

plot("~/Downloads/LocationHistory.kml")
