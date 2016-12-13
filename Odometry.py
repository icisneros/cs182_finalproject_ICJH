# Framework for generating noisy odometry data and keeping track of actual robot position in the world.

import random
import math

class Odometry:

	def __init__(self, trueMap, start_x=500, start_y=200, error = .03):

		# actualPosition is stored as pixels! Not meters!
		self.actualPosition = [start_y, start_x];  # in row, col format
		self.ERROR = error # this is given as the standard deviation of Gaussian noise per meter
		self.TRUE_MAP = trueMap.getTrueMap()
		self.SCALE = trueMap.getScale()
		self.MAP_OBJ = trueMap

		print "Odometer Initialized"


	# Updates the actual pose based on a movement command and returns a pose delta based on noisy odometry data.
	# Delta should be a list of the values to add to the current pose [y, x]
	# Returns None if the move would put the robot through a wall.
	def updatePosition(self, delta):
		dy = delta[0]
		dx = delta[1]

		if self.TRUE_MAP[self.actualPosition[0] + dy][self.actualPosition[1] + dx] == 1:
			return None 

		self.actualPosition[0] += dy
		self.actualPosition[1] += dx

		# print self.actualPosition

		# generate noisy odometry data
		dy = random.gauss(delta[0], abs(dy) * (self.ERROR/self.SCALE)) # divide error by scale to keep things in pixels
		dx = random.gauss(delta[1], abs(dx) * (self.ERROR/self.SCALE))

		return (dy, dx)

	def getActualPosition(self):
		return self.actualPosition

	def getError(self):
		return self.ERROR

