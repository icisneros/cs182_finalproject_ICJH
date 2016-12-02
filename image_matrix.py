import numpy as np
import scipy.misc



if __name__ == '__main__':
	the_map = scipy.misc.imread("MD_0_bw.png")
	# the_map = the_map.convert('1')
	print the_map.shape
	print the_map