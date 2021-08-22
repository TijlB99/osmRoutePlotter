from collections import defaultdict
from dotutils.densitymap import *
from datetime import datetime
import numpy as np
import math


def groupByDate(data, nb):
	groups = defaultdict(list)
	for dat in data:
		groups[dat[3][:nb]].append(dat)
	
	return groups

def removeCloseAndFarPoints(data, minThreshold, maxThreshold):
	result = [data[0]]
	for i in range(len(data)):
		if i > 0:
			v1 = result[-1][:2]
			v2 = data[i][:2]
			dist = [(float(a) - float(b))**2 for a, b in zip(v1, v2)]
			dist = math.sqrt(sum(dist))
			if dist > minThreshold and dist < maxThreshold:
				result.append(data[i])
	return np.array(result)
	
def splitOnDist(data, maxThreshold, dMap):
	result = [[data[0]]]
	j = 0
	for i in range(len(data)):
		if i > 0:
			v1 = result[j][-1][:2]
			v2 = data[i][:2]
			dist = [(float(a) - float(b))**2 for a, b in zip(v1, v2)]
			dist = math.sqrt(sum(dist))
			density = dMap.getDensity(float(data[i][0]), float(data[i][1]))
			
			if (dist > (maxThreshold * max(0.1, (1/density))) or getTimeDiffH(result[j][-1], data[i]) > 2):
				j += 1
				result.append([data[i]])
			else:
				result[j].append(data[i])
	return [np.array(res) for res in result]
	
def getTimeDiffH(d0, d1):
	t0 = d0[3]
	t1 = d1[3]
	FMT = '%Y-%m-%d %H:%M:%S'
	timeDelta = datetime.strptime(t1, FMT) - datetime.strptime(t0, FMT)
	return timeDelta.seconds/3600

def getBounds(res):
	minx = np.min(res[:,0].astype(float))
	miny = np.min(res[:,1].astype(float))
	maxx = np.max(res[:,0].astype(float))
	maxy = np.max(res[:,1].astype(float))
	return minx, maxx, miny, maxy