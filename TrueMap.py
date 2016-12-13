from conv_to_bin_mat import ConvBinMap

class TrueMap:
	
	def __init__(self, floorplan = "BinaryMaps/MD_MINI_binary.png", plan_scale = .04805):
		# Store true map. The map is indexed (0,0) in the top left with the form (y,x) (aka row, column)
		self.FLOORPLAN = floorplan
		self.TRUE_MAP = ConvBinMap.map_to_mat(floorplan) # returns np binary array of floorplan
		self.SCALE = plan_scale # meters per pixel

		# a list of tuples of legal positions
		self.LEGAL_POS = []
		rows,cols = self.TRUE_MAP.shape
		for row in range(rows):
			for col in range(cols):
				if self.TRUE_MAP[row][col] != 1:
					self.LEGAL_POS.append((row,col))

		self.NUM_LEGAL_POS = len(self.LEGAL_POS)

	def getFloorPlanFile(self):
		""" Returns the filepath to the floorplan
		"""
		return self.FLOORPLAN

	def getDimensions(self):
		""" Returns the dimensions of the map matrix in (row,col) format
		"""
		return self.TRUE_MAP.shape

	def getLegalPositions(self):
		""" Returns a list of tuples of rows and cols of all of the legal positions (elements in the 
			matrix that are not equal to 1, where 1 indicates the presence of a wall or obstacle).
			e.g. self.LEGAL_POS = [(row1,col1), (row2,col2)]
		"""
		return self.LEGAL_POS

	def getTrueMap(self):
		return self.TRUE_MAP

	def getScale(self):
		return self.SCALE

	def imposeMapLimits(self, x_pos, y_pos):
		""" Necessary in order to make sure that a coordinate does not go out-of-bounds
			or takes on a value that is right on the edge of the map.

			Map coordinates are indexed at 0, the the max value that a positions
			coordinate can take is map_rows - 1, map_cols - 1.
		"""

		map_rows, map_cols = self.getDimensions()
		
		if y_pos >= map_rows:
			y_pos = map_rows - 1
		if y_pos < 0:
			y_pos = 0
		if x_pos >= map_cols:
			x_pos = map_cols - 1
		if x_pos < 0:
			x_pos = 0

		return x_pos, y_pos

	def getOccupancyFraction(self):
		""" Returns the fraction of occupied (black, 1) pixels on the map
		"""
		total_pixels = self.TRUE_MAP.size
		num_legal = len(self.LEGAL_POS)
		num_occupied = total_pixels - num_legal

		return num_occupied / float(total_pixels)


