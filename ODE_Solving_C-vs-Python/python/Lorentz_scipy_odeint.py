import numpy as np
import pylab as pl
from scipy.integrate import odeint

def f(y,t):
    dy1 = sigma*(y[1] - y[0])
    dy2 = y[0]*(rho - y[2]) - y[1]
    dy3 = y[0]*y[1] - beta*y[2]
    return [dy1, dy2, dy3] 


tf = 3000
np1 = 100
t  = np.linspace(0, tf, tf*np1)
y0 = [1.,1.,1.]

sigma = 10.
rho = 28.
beta = 8./3.

soln = odeint(f, y0, t, rtol=1e-6, atol=1e-9)

y1 = soln[:,0]
y2 = soln[:,1]
y3 = soln[:,2]

#f, (ax1, ax2, ax3) = pl.subplots(3, sharex = True)
#ax1.plot(y1, y2)
#ax2.plot(y2, y3)
#ax3.plot(y1, y3)
#pl.show()
