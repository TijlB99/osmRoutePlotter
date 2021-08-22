from io import BytesIO
import urllib.request
from PIL import Image
import math

def lats2nums(lats, zoom):
	ytiles = []
	for lat_deg in lats:
		ytiles.append(lat2num(lat_deg, zoom))
	return ytiles

def lons2nums(lons, zoom):
	xtiles = []
	for lon_deg in lons:
		xtiles.append(lon2num(lon_deg, zoom))
	return xtiles

def lat2num(lat, zoom):
	n = 2.0 ** zoom
	lat_rad = math.radians(lat)
	return n * (1.0 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2.0

def lon2num(lon, zoom):
	n = 2.0 ** zoom
	return n * (lon + 180.0) / 360.0

def deg2num(lat, lon, zoom):
	xtile = int(lon2num(lon, zoom))
	ytile = int(lat2num(lat, zoom))
	return (xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
	n = 2.0 ** zoom
	lon = (xtile * 360.0) / n - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2.0 * ytile / n)))
	lat = lat_rad * 180 / math.pi
	return (lat, lon)
  
    
def getImageCluster(lon_deg, lon_max, lat_deg, lat_max, zoom, smurl):
	xmin, ymax =deg2num(lat_deg, lon_deg, zoom)
	xmax, ymin =deg2num(lat_max, lon_max, zoom)
	
	Cluster = Image.new('RGB',((xmax-xmin+1)*256,(ymax-ymin+1)*256), (255,0,0) ) 
	for xtile in range(xmin, xmax+1):
		for ytile in range(ymin,  ymax+1):
			try:			
				imgurl=smurl.format(zoom, xtile, ytile)
				request = urllib.request.Request(imgurl)
				request.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3")
				with urllib.request.urlopen(request) as url:
					imgstr = url.read()
				tile = Image.open(BytesIO(imgstr))
				Cluster.paste(tile, box=((xtile-xmin)*256, (ytile-ymin)*256))
			except Exception as e: 
				print("Couldn't download image:", e)

	return Cluster, (xmin, xmax + 1, ymax + 1, ymin) 
    
