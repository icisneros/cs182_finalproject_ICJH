#!/usr/bin/env python

"""
Show how to connect to keypress events
"""
import sys
import numpy as np
import matplotlib.pyplot as plt



def press(event):
	counter = 0
	# print('press', event.key)
	print 'press: ', event.key
	sys.stdout.flush()
	if event.key == 'x':
		counter += 1
		sys.stdout.write(str(counter) + '\n')
		visible = xl.get_visible()
		xl.set_visible(not visible)
		fig.canvas.draw()
	# print(counter)
	print counter



counter = 0

fig, ax = plt.subplots()

fig.canvas.mpl_connect('key_press_event', press)

ax.plot(np.random.rand(12), np.random.rand(12), 'go')
xl = ax.set_xlabel('easy come, easy go')

plt.show()