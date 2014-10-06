##
#  Plotting a neat contour plot with Matplotlib
#  This plot is currently the same used in one of the examples from pylab.
#  I should change it soon, but this is a first step for this example.
#  
#  by ThMosqueiro @ October 2014
##

import numpy as np
import random as rand
import pylab as pl



# Plotting the contour plot
delta = 0.01
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = pl.mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = pl.mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
Z = 10.0 * (Z2 - Z1)


# Here we are defining the value of each level
levels    = [-1.0, -0.5, -0.2, 0., 0.2, 0.5, 1.]
setcolors = ['#9999FF', '#6600BB', '#009900', '#006600', '#FF0066', '#FF0000', '#660000']


# Finally plotting
CS = pl.contour(X,Y,Z, levels=levels, colors=setcolors, linewidths=2.)


# Inserting labels
manual_locations = [(-3, -15), (-2, -14), (0, -14), (0, -10), (3.0, -10), (10., -10.), (7., -4)]
labelcolors = ['black', 'black', 'black', 'black', 'black', 'black', 'black']
pl.clabel(CS, inline=1, fontsize=13, manual=manual_locations, colors=labelcolors)

# Defining axis' labels
pl.xlabel('X')
pl.ylabel('Y')

# Creating the colorbar
pl.colorbar()

# Showing the plot
pl.show()
