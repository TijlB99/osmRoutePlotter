import numpy as np

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
	
	return np.array(result)