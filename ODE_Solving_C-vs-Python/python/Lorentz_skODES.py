# 
# I'm calling Sundials' CVODE using scikits.odes library. 
#
# TODO:
#    Make some comments
#    Test time tomorrow!
# 

from __future__ import print_function
import numpy as np
from scikits.odes import ode


# RHS of the Lorentz system's equations
def f(t, Y, Ydot):
    x = Y[0]
    y = Y[1]
    z = Y[2]
    
    Ydot[0] = sigma*(y - x)
    Ydot[1] = x*(rho - z) - y
    Ydot[2] = x*y - beta*z
    
    return Ydot



# ODE parameters
sigma = 10.
rho = 28.
beta = 8./3.

# Initial conditions
Y0 = [1., 1., 1.]


# Instantiating the integrator
solver = ode('cvode', f, rtol = 1e-6, atol = 1e-9)

# Total simulation time
tf = 3000.

# Times at which we want the output
t = np.linspace(0., tf, 100*int(tf))


# Integrating the Lorentz system
results = solver.solve(t, Y0)

# Writing output to a file
Youtput = np.zeros( (len( results[1] ), 4) )
Youtput[:,0] = results[1]
Youtput[:,1] = results[2][:,0]
Youtput[:,2] = results[2][:,1]
Youtput[:,3] = results[2][:,2]
np.savetxt('lorentz_output.dat', Youtput)
