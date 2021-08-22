import matplotlib.pyplot as plt
from math import floor
import numpy as np
import os

class DensityMap():

	def __init__(self, data, nbBinsPerAxis, rescaleFunction=lambda a: a):
		dMap = np.zeros((nbBinsPerAxis, nbBinsPerAxis))
		x = data[:,0].astype(float)
		y = data[:,1].astype(float)
		minX = np.min(x)
		rangeX = np.max(x) - minX + 1e-12
		minY = np.min(y)
		rangeY = np.max(y) - minY + 1e-12
		self.opt = (minX, minY, rangeX, rangeY, nbBinsPerAxis)
		x, y = self.scale(x,y)
		
		for i in range(len(dMap)):
			for j in range(len(dMap[i])):
				nb = ((i <= x) & (x < i + 1) & (j <= y) & (y < j + 1)).sum()
				dMap[i][j] = nb
		
		self.dMap = rescaleFunction(dMap)
		
	def scale(self, x, y):
		minX, minY, rangeX, rangeY, nbPinsPA = self.opt
		x -= minX
		x *= nbPinsPA / rangeX
		y -= minY 
		y *= nbPinsPA / rangeY
		return x, y
		
	def getDensity(self, lat, lon):
		x, y = self.scale(lat, lon)
		return self.dMap[floor(x)][floor(y)]

	def draw(self, path):
		plt.imshow(np.rot90(self.dMap), interpolation='none')
		plt.axis('off')
		plt.gca().set_aspect('equal', adjustable='box')
		plt.savefig(path, bbox_inches=0)
		plt.clf()
		