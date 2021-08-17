from io import BytesIO
import urllib.request
from PIL import Image
import math

def lats2nums(lats, zoom):
	ytiles = []
	n = 2.0 ** zoom
	for lat_deg in lats:
		lat_rad = math.radians(lat_deg)
		ytiles.append(n * (1.0 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2.0)
	return ytiles

def lons2nums(lons, zoom):
	xtiles = []
	n = 2.0 ** zoom
	for lon_deg in lons:
		xtiles.append(n * (lon_deg + 180.0) / 360.0)
	return xtiles

def deg2num(lat_deg, lon_deg, zoom):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile = int(n * (lon_deg + 180.0) / 360.0)
	ytile = int(n * (1.0 - (math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi)) / 2.0)
	return (xtile, ytile)
  
def num2deg(xtile, ytile, zoom):
	n = 2.0 ** zoom
	lon_deg = (xtile * 360.0) / n - 180.0
	lat_rad = math.atan(math.sinh(math.pi * (1 - 2.0 * ytile / n)))
	lat_deg = lat_rad * 180 / math.pi
	return (lat_deg, lon_deg)
  
    
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
    
