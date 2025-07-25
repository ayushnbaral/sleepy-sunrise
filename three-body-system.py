import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# -- Constants -- #
G = 6.67430e-11
dt = 3600  # 1 hour
M_sun = 1.989e30
M_earth = 5.972e24
M_moon = 7.348e22
AU = 1.496e11
r_earth_sun = AU
r_moon_earth = 3.84e8

# Simulation duration
total_days = 365
num_frames = int((total_days * 24 * 3600) / dt)

# Initial orbital speeds
v_earth = np.sqrt(G * M_sun / r_earth_sun)
v_moon = np.sqrt(G * M_earth / r_moon_earth)

# Toggle zoom on Earth
zoom_on_earth = True  # Set to False to view the full Sun-Earth-Moon system

# -- Plot setup -- #
fig, ax = plt.subplots()
ax.set_aspect('equal')
fig.set_facecolor('black')
ax.set_facecolor('black')
ax.set_title("Sun-Earth-Moon System", color='white')
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_edgecolor('white')

# Initial axis limits
if not zoom_on_earth:
    ax.set_xlim(-1.25 * AU, 1.25 * AU)
    ax.set_ylim(-1.25 * AU, 1.25 * AU)

# Celestial bodies
earth_dot, = ax.plot([], [], 'bo', markersize=8, label='Earth')
moon_dot, = ax.plot([], [], 'wo', markersize=4, label='Moon')
sun_dot, = ax.plot(0, 0, 'yo', markersize=12, label='Sun')

# Initial positions
pos_sun = np.array([0.0, 0.0])
pos_earth = np.array([r_earth_sun, 0.0])
pos_moon = pos_earth + np.array([0.0, r_moon_earth])

# Initial velocities
vel_earth = np.array([0.0, v_earth])
vel_moon = vel_earth + np.array([v_moon, 0.0])  # Orbiting Earth

def init():
    earth_dot.set_data([], [])
    moon_dot.set_data([], [])
    return earth_dot, moon_dot, sun_dot

def update(frame):
    global pos_earth, vel_earth, pos_moon, vel_moon

    # Forces
    r_es = pos_earth - pos_sun
    f_earth = -G * M_sun * M_earth / np.linalg.norm(r_es)**3 * r_es

    r_me = pos_moon - pos_earth
    f_moon_from_earth = -G * M_earth * M_moon / np.linalg.norm(r_me)**3 * r_me

    r_ms = pos_moon - pos_sun
    f_moon_from_sun = -G * M_sun * M_moon / np.linalg.norm(r_ms)**3 * r_ms

    # Accelerations
    a_earth = f_earth / M_earth
    a_moon = (f_moon_from_earth + f_moon_from_sun) / M_moon

    # Euler update
    vel_earth += a_earth * dt
    vel_moon += a_moon * dt
    pos_earth += vel_earth * dt
    pos_moon += vel_moon * dt

    # Dynamic zoom if toggled on
    if zoom_on_earth:
        ax.set_xlim(pos_earth[0] - 1e9, pos_earth[0] + 1e9)
        ax.set_ylim(pos_earth[1] - 1e9, pos_earth[1] + 1e9)

    # Set positions
    earth_dot.set_data([pos_earth[0]], [pos_earth[1]])
    moon_dot.set_data([pos_moon[0]], [pos_moon[1]])
    return earth_dot, moon_dot, sun_dot

# Animate
ani = FuncAnimation(fig, update, init_func=init, frames=num_frames, interval=15, blit=True)
ax.legend(facecolor='black', labelcolor='white', loc='upper left')
plt.show()
