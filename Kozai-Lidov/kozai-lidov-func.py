import rebound
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

sim = rebound.Simulation()
sim.units = ('yr', 'AU', 'Msun')
sim.add(m=1.0) #central
sim.add(m=1e-3, a=1.0, e=0.05) #inner
sim.add(m=0.01, a=10.0, inc=np.radians(65.0)) #outer
sim.move_to_com()
sim.integrator="ias15"

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(projection='3d')
ax.view_init(elev=30, azim=120)
fig.patch.set_facecolor('#010b19')
ax.set_facecolor('#010b19')
ax.set_xlim3d([-12, 12])
ax.set_ylim3d([-12, 12])
ax.set_zlim3d([-12, 12])
trail_length = 6

star_pos = ([], [], [])
inner_pos = ([], [], [])
outer_pos = ([], [], [])
star_trail_pos = ([], [], [])
inner_trail_pos = ([], [], [])
outer_trail_pos = ([], [], [])

star_dot, = ax.plot([0], [0], [0], color='red', marker='o', markersize=10)
inner_dot, = ax.plot([0], [0], [0], color='blue', marker='o', markersize=6)
outer_dot, = ax.plot([0], [0], [0], color='green', marker='o', markersize=7.33)
star_trail, = ax.plot([0], [0], [0], color='red', lw=5, alpha=0.5)
inner_trail, = ax.plot([0], [0], [0], color='blue', lw=5, alpha=0.5)
outer_trail, = ax.plot([0], [0], [0], color='green', lw=5, alpha=0.1)
updating_text = ax.text2D(0.02,0.95, "",transform=ax.transAxes, color="white")

time = np.arange(0,108573, 1.2)
index = np.linspace(0, len(time)-1, 5000, dtype=int)
orbit1_e = []

for i in time:
    sim.integrate(i)
    orbit1 = sim.orbits()[0]
    orbit2 = sim.orbits()[1]
    mut = np.arccos(np.cos(orbit1.inc) * np.cos(orbit2.inc) +
                    np.sin(orbit1.inc) * np.sin(orbit2.inc) * np.cos(orbit1.Omega - orbit2.Omega))
    star_pos[0].append(sim.particles[0].x)
    star_pos[1].append(sim.particles[0].y)
    star_pos[2].append(sim.particles[0].z)
    inner_pos[0].append(sim.particles[1].x)
    inner_pos[1].append(sim.particles[1].y)
    inner_pos[2].append(sim.particles[1].z)
    outer_pos[0].append(sim.particles[2].x)
    outer_pos[1].append(sim.particles[2].y)
    outer_pos[2].append(sim.particles[2].z)
    orbit1_e.append(orbit1.e)
    print((i / 10857) * 100)


def update(frame):
    actual_index = index[frame]
    star_dot.set_data([star_pos[0][actual_index]], [star_pos[1][actual_index]])
    star_dot.set_3d_properties([star_pos[2][actual_index]])
    inner_dot.set_data([inner_pos[0][actual_index]], [inner_pos[1][actual_index]])
    inner_dot.set_3d_properties([inner_pos[2][actual_index]])
    outer_dot.set_data([outer_pos[0][actual_index]], [outer_pos[1][actual_index]])
    outer_dot.set_3d_properties([outer_pos[2][actual_index]])
    star_trail.set_data(star_pos[0][max(0, actual_index - trail_length):actual_index], star_pos[1][max(0, actual_index - trail_length):actual_index])
    star_trail.set_3d_properties(star_pos[2][max(0, actual_index - trail_length):actual_index])
    inner_trail.set_data(inner_pos[0][max(0, actual_index - trail_length):actual_index], inner_pos[1][max(0, actual_index - trail_length):actual_index])
    inner_trail.set_3d_properties(inner_pos[2][max(0, actual_index - trail_length):actual_index])
    outer_trail.set_data(outer_pos[0][max(0, actual_index - trail_length):actual_index], outer_pos[1][max(0, actual_index - trail_length):actual_index])
    outer_trail.set_3d_properties(outer_pos[2][max(0, actual_index - trail_length):actual_index])
    current_time = time[actual_index]
    current_eccentricity = orbit1_e[actual_index]
    updating_text.set_text(f"Eccentricity: {current_eccentricity}, Time: {current_time}")



    return star_dot, inner_dot, outer_dot, updating_text

ani = FuncAnimation(fig, update, frames=2000, interval=15)
plt.show()
