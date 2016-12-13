from Odometry import Odometry
from ParticleFilter import ParticleFilter
from Sensor import Sensor
from TrueMap import TrueMap
from visualization import Visualization
import time
import math
from RobotMap import RobotMap



if __name__ == '__main__':

	# Initialize ***

	# coordinates in the middle of a room
	initx = 170
	inity = 150

	the_true_map = TrueMap(floorplan='BinaryMaps/MD_0_binary.png')

	# the_true_map = TrueMap()
	viz = Visualization(the_true_map, start_x=initx, start_y=inity)
	sensor = Sensor(the_true_map)
	odom = Odometry(the_true_map, start_x=initx, start_y=inity)
	part_filt = ParticleFilter(the_true_map, sensor, odom, numParticles=100)
	part_filt.initParticlesSpecific(initx, inity)

	the_robot_map = RobotMap(part_filt, posteriorProb=the_true_map.getOccupancyFraction())


	scale = 7  # number of pixels to move each time a movement is given
	# assuming a move command represents a 1 pixel move
	moveCommandDeltas = {'a':(0, -scale), 'w':(-scale, 0), 's':(scale, 0),'d':(0, scale), 'aw':(-scale, -scale), 'wa':(-scale,-scale),
						'wd':(-scale, scale) , 'dw':(-scale, scale) , 'sd':(scale,scale), 'ds':(scale,scale),
						'as':(scale, -scale), 'sa':(scale, -scale)}

	# Do some stuff ***
	viz.replot_particles(part_filt.getParticleLocations())
	viz.display_plot()

	step_count = 0

	while True:
		direction = raw_input("Move command: ")
		direction.lower()
		step_count += 1

		startTime = time.time() # determine amount of time for particle update
		# process the movement as a change in position
		if direction in moveCommandDeltas:
			odomMeasure = odom.updatePosition(moveCommandDeltas[direction])
			if odomMeasure is not None:
				part_filt.moveParticles(odomMeasure)

		sensor_readings = sensor.getNoisyDistances(odom.getActualPosition())
		sensor_angles = sensor.getSensorAngles()
		sensor_angles_rads = [math.radians(angle) for angle in sensor_angles]
		part_filt.weightParticles(sensor_readings)

		# Update the robot map using particle filter knowledge
		the_robot_map.updateMap(sensor_angles, sensor_readings)

		endTime = time.time()

		print "Time per particle without visualization: ", (endTime-startTime)/part_filt.getNumParticles()
		# visualize the particles every 10 steps
		# if step_count % 10 == 0:
		# 	viz.replot_particles(part_filt.getParticleLocations())
		viz.replot_particles(part_filt.getParticleLocations())

		# update the visual position
		viz.move_robot(new_coord=odom.getActualPosition())


		viz.display_plot()
		if (step_count % 10) == 0:
			viz.display_a_matrix(the_robot_map.getMap())
		
		endTime = time.time()
