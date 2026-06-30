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

viewframe = 11

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(projection='3d')
ax.view_init(elev=20, azim=120)
fig.patch.set_facecolor('#010b19')
ax.set_facecolor('#010b19')
ax.set_xlim3d([-viewframe, viewframe])
ax.set_ylim3d([-viewframe, viewframe])
ax.set_zlim3d([-viewframe, viewframe])
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.zaxis.label.set_color('white')

ax.tick_params(colors='white', grid_color='#1f2d42')

ax.xaxis.set_pane_color((0.02, 0.1, 0.2, 0.5))
ax.yaxis.set_pane_color((0.02, 0.1, 0.2, 0.5))
ax.zaxis.set_pane_color((0.02, 0.1, 0.2, 0.5))

ax.grid(True, color='#1f2d42', linestyle='--', linewidth=0.5)

star_pos = ([], [], [])

star_dot, = ax.plot([0], [0], [0], color='red', marker='o', markersize=5)
inner_orbit_line, = ax.plot([], [], [], color='cyan', lw=1.5, alpha=0.7)
outer_orbit_line, = ax.plot([], [], [], color='red', lw=1.5, alpha=0.7)
updating_text = ax.text2D(0.02,0.95, "",transform=ax.transAxes, color="white")

time = np.arange(0,108573, 1.2)
index = np.linspace(0, len(time)-1, 5000, dtype=int)
theta = np.linspace(0, 2*np.pi, 100, dtype=int)
orbit1_a = []
orbit1_e = []
orbit1_inc = []
orbit1_Omega = []
orbit1_omega = []
orbit2_a = []
orbit2_e = []
orbit2_inc = []
orbit2_Omega = []
orbit2_omega = []

print("starting")

for i in time:
    sim.integrate(i)
    orbit1 = sim.orbits()[0]
    orbit2 = sim.orbits()[1]
    mut = np.arccos(np.cos(orbit1.inc) * np.cos(orbit2.inc) +
                    np.sin(orbit1.inc) * np.sin(orbit2.inc) * np.cos(orbit1.Omega - orbit2.Omega))

    orbit1_a.append(orbit1.a)
    orbit1_e.append(orbit1.e)
    orbit1_inc.append(orbit1.inc)
    orbit1_Omega.append(orbit1.Omega)
    orbit1_omega.append(orbit1.omega)
    orbit2_a.append(orbit2.a)
    orbit2_e.append(orbit2.e)
    orbit2_inc.append(orbit2.inc)
    orbit2_Omega.append(orbit2.Omega)
    orbit2_omega.append(orbit2.omega)
    print(f'{i / 108573 * 100:.3f}% done')

print("completed")

def get_ellipse_coords(a, e, inc, Omega, omega):
    nu = np.linspace(0, 2*np.pi, 150)
    r = (a * (1 - e ** 2)) / (1 + e * np.cos(nu))
    x_prime = r * np.cos(nu)
    y_prime = r * np.sin(nu)

    cos_Omega, sin_Omega = np.cos(Omega), np.sin(Omega)
    cos_omega, sin_omega = np.cos(omega), np.sin(omega)
    cos_inc, sin_inc = np.cos(inc), np.sin(inc)

    x = x_prime * (cos_Omega * cos_omega - sin_Omega * sin_omega * cos_inc) + \
        y_prime * (-cos_Omega * sin_omega - sin_Omega * cos_omega * cos_inc)

    y = x_prime * (sin_Omega * cos_omega + cos_Omega * sin_omega * cos_inc) + \
        y_prime * (-sin_Omega * sin_omega + cos_Omega * cos_omega * cos_inc)

    z = x_prime * (sin_omega * sin_inc) + \
        y_prime * (cos_omega * sin_inc)

    return x, y, z

def update(frame):
    actual_index = index[frame]
    current_time = time[actual_index]
    current_eccentricity = orbit1_e[actual_index]

    ex1, ey1, ez1 = get_ellipse_coords(
        orbit1_a[actual_index],
        orbit1_e[actual_index],
        orbit1_inc[actual_index],
        orbit1_Omega[actual_index],
        orbit1_omega[actual_index]
    )
    inner_orbit_line.set_data(ex1, ey1)
    inner_orbit_line.set_3d_properties(ez1)

    ex2, ey2, ez2 = get_ellipse_coords(
        orbit2_a[actual_index],
        orbit2_e[actual_index],
        orbit2_inc[actual_index],
        orbit2_Omega[actual_index],
        orbit2_omega[actual_index]
    )
    outer_orbit_line.set_data(ex2, ey2)
    outer_orbit_line.set_3d_properties(ez2)

    updating_text.set_text(f"Eccentricity: {current_eccentricity:.4f}, Time: {current_time:.1f}")

    return star_dot, inner_orbit_line, outer_orbit_line, updating_text

ani = FuncAnimation(fig, update, frames=2000, interval=15)
plt.show()


