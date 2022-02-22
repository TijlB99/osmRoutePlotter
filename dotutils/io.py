import numpy as np
import json
import datetime

def readKml(path):
	result = []
	f = open(path, "r")
	lines = f.readlines()
	for line in lines:
		if "when" in line:
			lastWhen = line.replace("<when>", "").replace("</when>", "").replace("\n", "").replace(" ", "").replace("Z", "").replace("T", " ")
		if "gx:coord" in line:
			coords = line.replace("<gx:coord>", "").replace("</gx:coord>", "").replace("\n", "").split(" ")[-3:]
			coords.append(lastWhen)
			result.append(np.array(coords))
	
	print(result)
	return np.array(result)

def readJson(path):
	result = []
	f = open(path, "r")
	data = json.load(f)
	for location in data["locations"]:
		FMT = '%Y-%m-%d %H:%M:%S'
		# dt = datetime.datetime.fromtimestamp(int(location["timestampMs"])//1000)
		# dt = datetime.datetime.strptime(location["timestamp"][:-5], '%y-%m-%dT%H:%M:%S')
		# result.append(np.array([location["longitudeE7"]/1e7, location["latitudeE7"]/1e7, 0, dt.strftime(FMT)]))
		result.append(np.array([location["longitudeE7"]/1e7, location["latitudeE7"]/1e7, 0, location["timestamp"].replace("T", " ").split(".")[0].split("Z")[0]]))

	return np.array(result)