import numpy as np
import math

class RobotMap:

	def __init__(self, particleFilter, posteriorProb=0.5, start_x=170, start_y=150, dimensions=(270,240), plan_scale=.04805, sensor_noise = .5):
		# Dimension is of form (#rows, #umns)
		self.LEARNING_RATE = .5 # weight to give new scan relative to old belief
		self.MAP = np.full(dimensions, posteriorProb)
		self.SENSOR_NOISE = sensor_noise
		self.PLAN_SCALE = plan_scale
		self.part_filt = particleFilter
		self.X_MAX = dimensions[1]
		self.Y_MAX = dimensions[0]
		self.SENSOR_RANGE = 8;

	def updateMap(self, scanAngles, scanRanges):
		supposedPosition = self.part_filt.getSupposedLocation()
		# Step 1: combine sigma due to sensor noise and sigma due to location uncertainty
		for i in range(len(scanAngles)):
			if scanRanges[i] < (self.SENSOR_RANGE - .1):
				# Find combined sigma of scanner and directional position uncertainty
				# print "Scan Angle: " , scanAngles[i]
				sigmaTotal = math.sqrt(np.square(self.SENSOR_NOISE) + np.square(self.part_filt.getParticleStdDevDirectional(scanAngles[i])))
				
				# Determine which pixels should be updated
				# print "Scan location second part: ", (scanRanges[i]/self.PLAN_SCALE) * math.sin(scanAngles[i])
				scanYLocation = supposedPosition[0] - (scanRanges[i]/self.PLAN_SCALE) * math.sin(scanAngles[i]) 
				scanXLocation = supposedPosition[1] + (scanRanges[i]/self.PLAN_SCALE) * math.cos(scanAngles[i])

				pixelsToUpdate = self.getPixelsOnLine((scanYLocation, scanXLocation), 8 * sigmaTotal, scanAngles[i])
				
				for pixel in pixelsToUpdate:
					if pixel[0] >= 0 and pixel[0] < self.Y_MAX and pixel[1] >= 0 and pixel[1] < self.X_MAX:
						oldProb = self.MAP[pixel[0]][pixel[1]]
						pixelRange = math.sqrt(np.square((supposedPosition[0] - pixel[0])) + np.square((supposedPosition[1] - pixel[1])))
						newProb = self.gaussian(scanRanges[i], sigmaTotal, pixelRange)
						self.MAP[pixel[0]][pixel[1]] = self.LEARNING_RATE * newProb + (1-self.LEARNING_RATE) * oldProb

		#print self.MAP
		return self.MAP


	def gaussian(self, mu, sigma, x):
		""" calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
		:param mu:    distance to the landmark
		:param sigma: standard deviation
		:param x:     distance to the landmark measured by the robot
		:return gaussian value
		"""
		# print "mu", mu
		# print "sigma", sigma
		# print "x", x
		# calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
		return math.exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))


	# Returns a set of pixel values that lie along a specified line
	def getPixelsOnLine(self, center, length, angle):
		"""
		CURRENTLY UNTESTED!!!!!
		"""
		distancesAlongLine = np.linspace(-length/2, length/2, length/self.PLAN_SCALE)
		pixels = set()
		for distance in distancesAlongLine:
			y = int(center[0] - distance * math.sin(angle) + .5)
			x = int(center[1] + distance * math.cos(angle) + .5)
			pixels.add((y,x))
		return pixels

	def getMap(self):
		return self.MAP

			


