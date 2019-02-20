import numpy as np
import matplotlib.pyplot as plt

'''
Consider running this 
in a terminal window
'''
def plotgraph(r, theta):
	#print(str(theta) + " , " + str(r))
    ax = plt.subplot(111, projection='polar')
    ax.set_rmax(200)
    ax.plot(theta, r)
    print(theta)
    print(r)
    ax.set_rmax(210)
    ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
    ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
    ax.grid(True)
    ax.set_title("Simulated Pattern", va='bottom')
    plt.show()

