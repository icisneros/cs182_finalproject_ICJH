import matplotlib.pyplot as plt

import matplotlib.animation as anim

INIT_X = 500
INIT_Y = 200

FLOORPLAN = "BinaryMaps/MD_0_binary.png"



def move_robot_plot(up,down,left,right, init_inst, last_loc):
	
	# must close all previous figures or else the function will eat up all the 
	# computer's memory
	plt.close("all")

	# Calculate the reference coordinate.  If this is the first plot, then the robot
	# will start at location (INIT_X, INIT_Y).  In this case, init_inst must
	# be equal to True.
	if init_inst:
		x_start, y_start = INIT_X, INIT_Y
	else:
		x_start, y_start = last_loc
	
	# each iteration creates a new figure to give the illusion of movement
	plt.figure()

	# the image of the floorplan onto which the dots will be overlayed
	im = plt.imread(FLOORPLAN)  # image of the floorplan

	im1 = plt.imshow(im, cmap=plt.cm.gray, interpolation='nearest')


	# scatter() takes values in [x][y] order (so the opposite of the numpy array ordering)
	# Overlay particles and the floorplan

	# # leftwards
	# for i in range(3):
	# 	plt.scatter([29 - i], [88], c='r', s=4)

	# # downwards
	# for i in range(8):
	# 	plt.scatter([29], [88 + i], c='r', s=4)

	# # rightwards
	# for i in range(70):
	# 	plt.scatter([29 + i], [88], c='r', s=4)

	# # upwards
	# for i in range(72):
	# 	plt.scatter([29], [88 - i], c='r', s=4)

	new_x = x_start + (left + right) * 20
	new_y = y_start + (up + down) * 20
	
	# The robot
	# put a blue dot, size 65, but actually consists of only its coordinate (new_x, new_y):
	plt.scatter(x=[new_x], y=[new_y], c='b', s=65)

	# must have block = False in order to allow for the script to continue
	plt.show(block=False)


	# last location of the robot
	return (new_x, new_y)



# For testing with the terminal:
if __name__ == '__main__':

	last_loc = move_robot_plot(0,0,0,0,True,(0,0))
	# ConvBinMap.map_to_binary_image()
	while True:
		direction = raw_input("Move command: ")
		direction.lower()

		if direction == 'w':
			last_loc = move_robot_plot(-1,0,0,0,False,last_loc)
		elif direction == 'a':
			last_loc = move_robot_plot(0,0,-1,0,False,last_loc)
		elif direction == 's':
			last_loc = move_robot_plot(0,1,0,0,False,last_loc)
		elif direction == 'd':
			last_loc = move_robot_plot(0,0,0,1,False,last_loc)


