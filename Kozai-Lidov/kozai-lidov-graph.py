import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.add(m=1.0) #central
sim.add(m=1e-3, a=1.0, e=0.05) #inner
sim.add(m=0.01, a=10.0, inc=np.radians(65.0)) #outer
sim.move_to_com()
sim.integrator="ias15"

list_e = []
time = []
constant = []
inc = []

for i in np.linspace(0, 108573, 2000, dtype=int):
    sim.integrate(i)
    orbit1 = sim.orbits()[0]
    orbit2 = sim.orbits()[1]
    mut = np.arccos(np.cos(orbit1.inc)*np.cos(orbit2.inc)+
                    np.sin(orbit1.inc)*np.sin(orbit2.inc)*np.cos(orbit1.Omega - orbit2.Omega))
    constant.append(np.sqrt(1 - orbit1.e**2) * np.cos(mut))
    list_e.append(orbit1.e)
    time.append(i)
    inc.append(np.degrees(mut))
    print(i)

plt.subplot(1,2,1)
plt.plot(time, list_e)
plt.plot(time, constant, 'r')
plt.legend(['Eccentricity', 'Constant'], loc='upper left')
plt.xlabel("Time (years)")
plt.subplot(1,2,2)
plt.plot(time, inc)
plt.show()

