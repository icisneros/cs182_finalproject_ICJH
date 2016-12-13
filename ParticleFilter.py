import numpy as np
import random
import copy
from numpy.random import choice
from numpy import ndarray
import math

class ParticleFilter:

	def __init__(self, trueMap, sensor, odometer, numParticles=1000):
		self.NUM_PARTICLES = numParticles
		self.TRUE_MAP = trueMap.getTrueMap()
		self.legalPositions = trueMap.getLegalPositions()
		self.NUM_LEGAL_POS = len(self.legalPositions)
		self.MOVEMENT_MODEL = odometer.getError()
		self.MAP_SCALE = trueMap.getScale()
		self.TRUE_SENSOR = sensor #for assigning weights to particles when wall locations are known
		self.SENSOR_NOISE = sensor.getNoise()
		self.MAP_DIMS = trueMap.getDimensions()
		self.MAP_OBJ = trueMap
		
		self.Particles = []  # characeristics of a particle: [position, ...]

		print "Particle filter initialized"


	def initializeParticles(self):
		""" Initializes a list of particles, where each particle is a list of positions and other features, 
		    and a particle's position is a list of the form [row,col] (or [y,x])

			Each particle position is a pixel location (equivalently, an element in the map matrix)

			If the number of legal positions is less than the default number of particles 'numParticles'
			then it redefines self.NUM_PARTICLES and distributes these uniformly only into legal positions
			(positions with no wall or obstacles)

			Otherwise it distributes numParticles number of particles randomly only into legal positions
			(positions with no wall or obstacles.)
		"""
		self.Particles = []

		if self.NUM_PARTICLES > self.NUM_LEGAL_POS:
			self.NUM_PARTICLES = self.NUM_LEGAL_POS

		# if num of particles is equal to the number of legal positions, then distribute uniformly
		# else distribute into random legal positions (this is due to a limit on number of particles,
		# which for most maps will be in the hundreds of thousands)
		if self.NUM_PARTICLES == self.NUM_LEGAL_POS:
			for p_row, p_col in self.legalPositions: 
				# position in positions
				self.Particles.append([[p_row, p_col]])
		else:
			# pick a random legal position
			legal_positions = copy.deepcopy(self.legalPositions)
			i = 0
			while i < self.NUM_PARTICLES:
				p_row, p_col = random.choice(legal_positions)
				legal_positions.remove((p_row,p_col))
				self.Particles.append([[p_row, p_col]])
				i += 1


	def initParticlesSpecific(self, locx, locy):
		""" Initializes a list of particles to a specific x, y location for use
		    in slam.

		    Each particle is a list of positions and other features, 
		    and a particle's position is a list of the form [row,col] (or [y,x])

			Each particle position is a pixel location (equivalently, an element in the map matrix)

			If the number of legal positions is less than the default number of particles 'numParticles'
			then it redefines self.NUM_PARTICLES and distributes these uniformly only into legal positions
			(positions with no wall or obstacles)
		"""
		self.Particles = []

		if self.NUM_PARTICLES > self.NUM_LEGAL_POS:
			self.NUM_PARTICLES = self.NUM_LEGAL_POS

		# all particle locations will be the same
		i = 0
		while i < self.NUM_PARTICLES:
			self.Particles.append([[locy, locx]])
			i += 1


	# update particles according to motion model. Update after each robot movement.
	# Motion model consists of odometry reading probability distribution and legality of new position
	def moveParticles(self, odometryReading):
		for i in range(self.NUM_PARTICLES):		
			
			dy = random.gauss(odometryReading[0], odometryReading[0] * self.MOVEMENT_MODEL/self.MAP_SCALE)
			dx = random.gauss(odometryReading[1], odometryReading[1] * self.MOVEMENT_MODEL/self.MAP_SCALE)
			y_pos = int(self.Particles[i][0][0] + dy + 1)
			x_pos = int(self.Particles[i][0][1] + dx + 1)

			# Map limits enforced
			x_pos, y_pos = self.MAP_OBJ.imposeMapLimits(x_pos, y_pos)

			self.Particles[i][0][0] = y_pos
			self.Particles[i][0][1] = x_pos


	# This is only used for localization when you know the map! Sensor reading is passed to this method to determine
	# probability of sensor reading given location P(e|X)
	def weightParticles(self, sensorReading):
		weight = [0] * self.NUM_PARTICLES
		for i in range(self.NUM_PARTICLES):
			y_pos = self.Particles[i][0][0]
			x_pos = self.Particles[i][0][1]
			trueRanges = self.TRUE_SENSOR.getTrueDistances([y_pos, x_pos])
			weight[i] = self.measurement_prob(trueRanges, sensorReading)

		norm_weight = [float(i)/sum(weight) for i in weight]

		newParticlesIndices = np.random.choice(range(len(self.Particles)), size = self.NUM_PARTICLES, replace = True, p = norm_weight)  # an array

		newParticles = []
		for i in range(len(newParticlesIndices)):
			newParticles.append(copy.deepcopy(self.Particles[newParticlesIndices[i]]))
		self.Particles = copy.deepcopy(newParticles)


	def getParticleLocations(self):
		""" Only to be used by the visualizer class.
		    Returns a list of particle locations in (y,x) format

		    e.g. particleLocations = [(y1,x1), (y2,x2), (y3,x3)]
		"""
		particleLocations = []
		for particle in self.Particles:
			p_row, p_col = particle[0]
			particleLocations.append((p_row, p_col))  # appended in (y,x) format

		return particleLocations


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


	def measurement_prob(self, trueRanges, sensorReading):
		""" Calculate the measurement probability: how likely a measurement should be
		:param measurement: current measurement
		:return probability
		"""

		prob = 1.0

		for i in range(len(trueRanges)):
			prob *= self.gaussian(trueRanges[i], self.SENSOR_NOISE, sensorReading[i])
		return prob

	def getNumParticles(self):
		return self.NUM_PARTICLES


	def getParticleStdDev(self):
		""" Standard deviation of a particle location using rms distance
		"""
		particleList = self.getParticleLocations()
		yList = [coord[0] for coord in particleList]
		xList = [coord[1] for coord in particleList]
		
		# convert to numpy arrays so that numpy stat methods can be used
		yarr = np.array(yList)  # yo ho yo ho, a pirate's life for me!
		xarr = np.array(xList)

		xMu = np.mean(xarr)
		yMu = np.mean(yarr)

		rms = 0
		for i in range(len(yarr)):
			rms += np.square((yarr[i]-yMu)) + np.square((xarr[i] - xMu))
		rms = math.sqrt(rms/len(yarr))


	def getParticleStdDevDirectional(self, theta):	
		particleList = self.getParticleLocations()
		yList = [coord[0] for coord in particleList]
		xList = [coord[1] for coord in particleList]
		
		# convert to numpy arrays so that numpy stat methods can be used
		yarr = np.array(yList)  # yo ho yo ho, a pirate's life for me!
		xarr = np.array(xList)

		combined = np.array([xarr, yarr])
		rotationMatrix = np.array([[math.cos(theta), math.sin(theta)],[-math.sin(theta), math.cos(theta)]])  # clockwise rotation

		rotatedPoints = np.matmul(rotationMatrix, combined)  # first row is all x values, second row is all y values

		stdDev = np.std(rotatedPoints[0])  # standard dev of only the x values (aka std deviation in direction of theta)
		# print "Standard deviation in direction ", theta, ": ", stdDev
		return stdDev

	def getSupposedLocation(self):
		""" Returns the average of the particle locations in y,x form
		"""
		#
		particleList = self.getParticleLocations()
		yList = [coord[0] for coord in particleList]
		xList = [coord[1] for coord in particleList]
		
		# convert to numpy arrays so that numpy stat methods can be used
		yarr = np.array(yList)  # yo ho yo ho, a pirate's life for me!
		xarr = np.array(xList)

		mean_x = np.mean(xarr)
		mean_y = np.mean(yarr)
		
		return (mean_y, mean_x)



