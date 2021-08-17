import matplotlib.pyplot as plt
import numpy as np
import os
	
def makeDensityMap(data, nbBinsPA):
	dMap = np.zeros((nbBinsPA, nbBinsPA))
	x = data[:,0].astype(float)
	y = data[:,1].astype(float)
	minX = np.min(x)
	rangeX = np.max(x) - minX + 1e-12
	minY = np.min(y)
	rangeY = np.max(y) - minY + 1e-12
	opt = (minX, minY, rangeX, rangeY, nbBinsPA)
	x, y = scale(x,y, opt)
	
	for i in range(len(dMap)):
		for j in range(len(dMap[i])):
			nb = ((i <= x) & (x < i + 1) & (j <= y) & (y < j + 1)).sum()
			dMap[i][j] = nb
	return dMap, opt
	
def scale(x, y, opt):
	minX, minY, rangeX, rangeY, nbPinsPA = opt
	x -= minX
	x *= nbPinsPA / rangeX
	y -= minY 
	y *= nbPinsPA / rangeY
	return x, y
	
def getDensity(data, dMap, opt):
	x, y = scale(float(data[0]), float(data[1]), opt)
	return dMap[floor(x)][floor(y)]

def drawDMap(dMap, path):
	plt.imshow(np.rot90(dMap), interpolation='none')
	plt.axis('off')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.savefig(path, bbox_inches=0)
	plt.clf()
	