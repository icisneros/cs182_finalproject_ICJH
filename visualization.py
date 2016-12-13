import matplotlib.pyplot as plt
import numpy as np

# for testing purposes
from conv_to_bin_mat import ConvBinMap
from TrueMap import TrueMap



class Visualization:
	""" Usage:
		intantiatate with Visualization()
			- can specify:
				- intiial robot coordinates using start_x and start_y
				- the floorplan image that is being used
				- the size of the robot representation
				- the size of the particle representations
				- the movement increments (1 if you want true movement, but 20 if you want faster movement)
		
		then use any of the functions other than 'display_plot' to specify the object/s to be drawn
		then use 'display_plot' to actually display the stuff


		Functions:
		'replot_particles' to plot particle dots

		'move_robot' to either move by keyboard command or when given a list of movements or a list of x,y coordinates

		'dart' is a function that just draws a line with specified start and stop coordinates and angle (for testing purposes)

		'display_plot' must be called after every 'replot_particles', 'move_robot', or 'dart', (or any sequential 
			         combination of these) or else you wont see the updated locations

	"""


	def __init__(self, trueMap, start_x=500, start_y=200, floorplan=None, rob_size=60, part_size=6, move_incr=4):
		# Map variables ***************
		# can pass in a trueMap object or expliitly define the floorplan filepath for testing purposes
		if floorplan is not None:
			self.FLOORPLAN = floorplan
			self.xmin = -100
			self.xmax = 1900
			self.ymin = -50
			self.ymax = 800
		else:
			self.FLOORPLAN = trueMap.getFloorPlanFile()  # the floorplan filepath
			# limits for the plot axes (in number of pixels)
			map_rows, map_cols = trueMap.getDimensions()
			self.xmin = 0
			self.xmax = map_cols
			self.ymin = 0
			self.ymax = map_rows

		self.IM = plt.imread(self.FLOORPLAN)  # image of the floorplan
		self.MAP_OBJ = trueMap


		# Robot variables ***************
		self.start_x = start_x  # robot's initial x coordinate
		self.start_y = start_y  # robot's initial y coordinate
		self.LAST_LOC = (start_x, start_y)  # the robot's last location (onto which the dots will be overlayed)
		self.INIT_INST = True  # whether this is the first usage of plot (important for the robot)
		self.RSIZE = rob_size  # diameter of the robot dot
		self.MOVINCR = move_incr  # the amount of pixels (matrix elements) that the robot will move
		self.MOVE_COMMS = []
		self.MOVE_COORD = []

		# Particle variables ***************
		self.PSIZE = part_size  # diameter of the particle dots
		self.PARTICLES = []  # a list of particle coordinates in (x,y) tuple form
		

		# Other ***************
		self.LINES = []  # a list of lists of tuples (endpoints of lines)


		print "Visualization engine initialized"



	def replot_particles(self, particlelist, numtoplot=100):
		""" Takes in a list of particle locations (one for each particle) and updates the self.PARTICLES variable:
			example: [(p1x, p1y), (p2x, p2y), (p3x, p3y)]

			Retains the locations of these particles, and updates the visual representation only when this 
			function is called and given a new list of locations.

			numtoplot limits the amount of particles that are actually plotted (because plotting more particles
			makes transition time between states slower).  Default to the first 100 particles.  If there are 
			fewer than numtoplot particles, then it plots all of them.
		"""
		# Overlay particles and the floorplan
		if len(particlelist) <= numtoplot:
			self.PARTICLES = particlelist
		else:
			for i in range(numtoplot):
				self.PARTICLES.append(particlelist[i])


	def move_robot(self, move_comm='k', new_coord=None, move_comm_list=[], move_coord_list = []):
		""" Given a movement command (string), new coordinate, or a list of movements for the robot, 
		    or a list of coordinates that it moved through, and updates the location of the robot dot.

		    move_comm is a string with directionality (standard wasd keyboard input)
		    e.g. 'w' = move north
		         'a' = move west
		         's' = move south
		    	 'd' = move move east
		    	 'aw' or 'wa' = move north west
		    	 'wd' or 'dw' = move north east
		    	 'sd' or 'ds' = move south east
		    	 'as' or 'sa' = move south west
		"""

		if new_coord is not None:  # if given a specific coordinate to move to
			new_y, new_x = new_coord
			self.LAST_LOC = (new_x, new_y)
		elif move_comm_list:  # if given a list of movement commands
			self.MOVE_COMMS = move_comm_list
		elif move_coord_list: # if given a list of movement coordinates
			self.MOVE_COORD = move_coord_list
		else:
			# For manual movement or automated movement via a command list

			# This initialization means that the robot will not move if not given a legitimate
			# keyboard direction
			x_dir = 0
			y_dir = 0

			if move_comm == 'w':
				x_dir = 0
				y_dir = -1
			elif move_comm == 'a':
				x_dir = -1
				y_dir = 0
			elif move_comm == 's':
				x_dir = 0
				y_dir = 1
			elif move_comm == 'd':
				x_dir = 1
				y_dir = 0
			elif move_comm == ('aw' or 'wa'):
				x_dir = -1
				y_dir = -1
			elif move_comm == ('wd' or 'dw'):
				x_dir = 1
				y_dir = -1
			elif move_comm == ('sd' or 'ds'):
				x_dir = 1
				y_dir = 1
			elif move_comm == ('as' or 'sa'):
				x_dir = -1
				y_dir = 1


			# Calculate the reference coordinate.  If this is the first plot, the robot
			# will start at location (start_x, start_y).  In this case, self.INIT_INST must
			# be equal to True
			if self.INIT_INST:
				x_start, y_start = self.start_x, self.start_y
				self.INIT_INST = False
			else:
				x_start, y_start = self.LAST_LOC

			new_x = x_start + (x_dir) * self.MOVINCR
			new_y = y_start + (y_dir) * self.MOVINCR

			self.LAST_LOC = (new_x, new_y)




	def dart(self, linelist):
		""" Takes in a list of lists of line endpoint locations and updates the self.LINES variable:
			example with two lines: [[(1,2),(3,4)],[(5,6),(7,8)]]

			Endpoints are given in the form [(start_x, start_y), (end_x, endy)]

			Retains the locations of these lines, and updates the visual representation only when this 
			function is called and given a new list of line endpoints.
		"""
		# Overlay particles and the floorplan
		self.LINES = linelist


	def display_plot(self):
		""" Uses matplotlib to create a figure with the floorplan overlayed with the
			dots representing the robot and the particles.

			MUST BE CALLED AFTER EVERY CALL OF replot_particles OR move_robot.  Otherwise
			the plot will not show.

			Can be optimized to be more memory efficient, but for the time being it works.
		"""
		# must close all previous figures or else the function will eat up all the 
		# computer's memory
		plt.close("all")

		# each iteration creates a new figure to give the illusion of movement
		plt.figure(figsize=(14,9))  # figsize specifies the window size (in inches)

		# the image of the floorplan onto which the dots will be overlayed
		im1 = plt.imshow(self.IM, cmap=plt.cm.gray, interpolation='nearest')

		axes = plt.gca()
		axes.set_xlim([self.xmin, self.xmax])
		axes.set_ylim([self.ymax, self.ymin])  # must be reversed in order to plot (0,0) on top left corner

		# Here's where the robot is actually plotted
		# put a blue dot, size self.RSIZE, but actually consists of only its coordinate (new_x, new_y):
		# scatter() takes values in [x][y] order (so the opposite of the numpy array ordering)
		if self.MOVE_COMMS:
			for command in self.MOVE_COMMS:
				self.move_robot(move_comm=command)
				rob_x, rob_y = self.LAST_LOC
				print "LAST_LOC: ", self.LAST_LOC
				plt.scatter(x=[rob_x], y=[rob_y], c='b', s=self.RSIZE)

			self.MOVE_COMMS = []
		elif self.MOVE_COORD:
			for coord in self.MOVE_COORD:
				self.move_robot(new_coord=coord)
				rob_x, rob_y = self.LAST_LOC
				print "LAST_LOC: ", self.LAST_LOC
				plt.scatter(x=[rob_x], y=[rob_y], c='b', s=self.RSIZE)

			self.MOVE_COORD = []
		else:
			rob_x, rob_y = self.LAST_LOC
			plt.scatter(x=[rob_x], y=[rob_y], c='b', s=self.RSIZE)

		# Here's where the particles are actually plotted
		# put a red dot, size self.PSIZE, but actually consists of only its coordinate (new_x, new_y):
		# scatter() takes values in x, y order (so the opposite of the numpy array ordering)
		if self.PARTICLES:
			for (py,px) in self.PARTICLES:
				plt.scatter(px, py, c='r', s=self.PSIZE)

			self.PARTICLES = []  # in order to make the visualization faster, it erases the particle list from memory 
								 # (only plots every time replot_particles)

		# Here's where the lines are actually plotted
		# requires a list of lists of start points and end points
		if self.LINES:
			for points in self.LINES:
				(startx, starty), (endx, endy) = points
				plt.plot([startx, endx], [starty, endy], 'k-', c='g',lw=2)


		# must have block = False in order to allow for the script to continue and accept more
		# user commands
		plt.show(block=False)


	def display_a_matrix(self, map_matrix):
		""" Given a numpy matrix, generates a map and displays it.
			Intended for displaying the generated map that the robot creates from its 
			SLAM procedure/exploration.

			Because of the dumb way that MatPlotLib plots matrices, the zeros and ones have
			to be flipped from the way that they are represented in every other class...
			Thus there's like a 2 second wait time for this function to actually display the
			matrix.

			Thus, in this case 0 = wall, 1 = empty area.
		"""

		# gotta flip the bits for some stupid reason
		# for (x,y), value in np.ndenumerate(map_matrix):
		# 	if map_matrix[x][y] == 0:  # empty area
		# 		map_matrix[x][y] = 1 
		# 	elif map_matrix[x][y] == 1:  # wall or obstacle
		# 		map_matrix[x][y] = 0 

		plt.matshow(map_matrix, fignum=100, cmap=plt.cm.gray)

		plt.show(block=False)





# For testing with the terminal:
if __name__ == '__main__':


	rand_mat = np.random.rand(100,100)

	# test the trueMap object
	testmap = TrueMap()
	c = Visualization(testmap, floorplan="BinaryMaps/MD_0_binary.png")

	# # testing the initial position and particle drawing function
	c.move_robot('k')  # k is meaningless to the parser
	# c.replot_particles([(29,88), (100,40), (700,390)])
	c.display_plot()

	# # test a list of keyboard commands
	# # movements = ['w', 'a', 's', 's', 's', 's']
	# # c.move_robot(move_comm_list=movements)
	# # c.display_plot()

	# # test moving according to a list of coords
	# # move straight down then take a right
	# coords = [(500,220), (500,240), (500,260), (500,220), (520,260), (540,260)]
	# c.move_robot(move_coord_list=coords)

	# test the line drawing functions
	# test_lines = [[(500,600), (550,580)],[(100,200), (100,300)]]
	# c.dart(test_lines)


	# test the matrix drawing function
	# test_mat = np.random.rand(64, 64)
	# test_mat = ConvBinMap.map_to_mat("BinaryMaps/MD_0_binary.png")

	c.display_a_matrix(rand_mat)

	while True:
		cont = raw_input('Press enter to continue the simulation: ')
		c.display_plot()
		c.display_a_matrix(rand_mat)
		# c.display_a_matrix(test_mat)

	# Give manual commands
	# while True:
	# 	c.display_plot()
	# while True:
	# 	direction = raw_input("Move command: ")
	# 	direction.lower()
	# 	c.move_robot(move_comm=direction)
	# 	c.display_plot()






