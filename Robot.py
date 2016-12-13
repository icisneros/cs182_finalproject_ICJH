from Odometry import Odometry
from ParticleFilter import ParticleFilter
from Sensor import Sensor
from TrueMap import TrueMap
from visualization import Visualization
import time



if __name__ == '__main__':

	# Initialize ***

	# coordinates in the middle of a room
	initx = 170
	inity = 150

	the_map = TrueMap(floorplan='BinaryMaps/MD_MINI_binary.png')
	# the_map = TrueMap()
	viz = Visualization(the_map, start_x=initx, start_y=inity)
	sensor = Sensor(the_map)
	odom = Odometry(the_map, start_x=initx, start_y=inity)
	part_filt = ParticleFilter(the_map, sensor, odom, numParticles=100)
	part_filt.initializeParticles()

	scale = 7  # number of pixels to move each time a movement is given
	# assuming a move command represents a 1 pixel move
	moveCommandDeltas = {'a':(0, -scale), 'w':(-scale, 0), 's':(scale, 0),'d':(0, scale), 'aw':(-scale, -scale), 'wa':(-scale,-scale),
						'wd':(-scale, scale) , 'dw':(-scale, scale) , 'sd':(scale,scale), 'ds':(scale,scale),
						'as':(scale, -scale), 'sa':(scale, -scale)}

	# Do some stuff ***
	viz.replot_particles(part_filt.getParticleLocations(), numtoplot=100)
	viz.display_plot()

	step_count = 0

	while True:
		direction = raw_input("Move command: ")
		direction.lower()

		step_count += 1

		# startTime = time.time() # determine amount of time for particle update
		# process the movement as a change in position
		if direction in moveCommandDeltas:
			odomMeasure = odom.updatePosition(moveCommandDeltas[direction])
			if odomMeasure is not None:
				part_filt.moveParticles(odomMeasure)

		sensor_readings = sensor.getNoisyDistances(odom.getActualPosition())
		part_filt.weightParticles(sensor_readings)
		# endTime = time.time()
		# print "Total time for particle update without visualizaztion: ", endTime-startTime
		# print "Time per particle without visualization: ", (endTime - startTime)/part_filt.getNumParticles()
		# print sensor.convertToRelativeCartesian(sensor_readings)

		# part_filt.getParticleStdDev()

		# visualize the particles every 10 steps
		if step_count % 10 == 0:
			viz.replot_particles(part_filt.getParticleLocations(), numtoplot=500)
		# viz.replot_particles(part_filt.getParticleLocations(), numtoplot=500)



		# update the visual position
		viz.move_robot(new_coord=odom.getActualPosition())


		viz.display_plot()
		# endTime = time.time()
		# print "Total time for particle update with visualizaztion: ", endTime-startTime
		# print "Time per particle with visualization: ", (endTime - startTime)/part_filt.getNumParticles()
