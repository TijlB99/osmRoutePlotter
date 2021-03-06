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
	for i in range(1, len(data)):	
		v1 = result[-1][:2]
		v2 = data[i][:2]
		dist = distance(v1,v2)
		if dist > minThreshold and dist < maxThreshold:
			result.append(data[i])
	return np.array(result)
	
def removeJumps(data, threshold):
	result = [data[0]]
	for i in range(1, len(data) - 1):
		p1, p2, p3 = data[i - 1], data[i], data[i + 1]
		if distance(p1, p3) / (distance(p1, p2) + 1e-10) >= threshold:
			result.append(data[i])
	result.append(data[-1])
	return np.array(result)

	
def splitOnDist(data, maxThreshold, dMap):
	result = [[data[0]]]

	for i in range(1, len(data)):
		v1 = result[-1][-1][:2]
		v2 = data[i][:2]
		dist = distance(v1,v2)
		density = dMap.getDensity(float(data[i][0]), float(data[i][1]))
		
		if (dist > (maxThreshold * max(0.1, (1/density))) or getTimeDiffH(result[-1][-1], data[i]) > 2):
			result.append([data[i]])
		else:
			result[-1].append(data[i])
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

def distance(p1, p2):
	return  (((float(p2[0]) - float(p1[0]))**2) + ((float(p2[1])-float(p1[1]))**2) )**0.5
