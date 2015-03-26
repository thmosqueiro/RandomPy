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

sigma = 10.
rho = 28.
beta = 8./3.
Y0 = [1., 1., 1.]

#define function for the right-hand-side equations which has specific signature
def f(t, Y, Ydot):
    x = Y[0]
    y = Y[1]
    z = Y[2]
    
    Ydot[0] = sigma*(y - x)
    Ydot[1] = x*(rho - z) - y
    Ydot[2] = x*y - beta*z
    
    return Ydot
    
solver = ode('cvode', f)

tf = 30.
t = np.linspace(0., tf, 100*int(tf))
results = solver.solve(t, Y0)

t = results[1]
x = results[2][:,0]
y = results[2][:,1]
z = results[2][:,2]

for j in range(len(t)):
    print('%4.2f %15.6g %15.6g %15.6g' % (t[j], x[j], y[j], z[j]) )
