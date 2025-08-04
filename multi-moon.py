import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Zoom scale (Jupiter system is much smaller than the Solar System)
lim = 4e9  # ~4 million km
dt = 10  # Time step in seconds (~17 minutes)

plt.rcParams['font.family'] = 'cambria'
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.view_init(elev=30, azim=120)
fig.patch.set_facecolor('#010b19')   # Deep navy
ax.set_facecolor('#010b19')          # Axis face background
ax.grid(False)
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.set_pane_color((1, 1, 1, 0))  # Make panes fully transparent
    axis._axinfo["grid"]['color'] =  (0, 0, 0, 0)  # Hide gridlines
ax.set_title("Jupiter and Galilean Moons", color='white')

# -- Jupiter and Moon Data -- #
moon_data = {
    "jupiter": [1.898e27, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
}

# Orbital parameters for moons: [mass, orbital_radius, orbital_speed, inclination]
orbital_params = {
    # Galilean moons
    "io":        [8.93e22,   421.7e6,   17340.0, 0.036],
    "europa":    [4.80e22,   671.1e6,   13740.0, 0.47],
    "ganymede":  [1.48e23,   1.0704e9,  10880.0, 0.20],
    "callisto":  [1.08e23,   1.8827e9,  8200.0,  0.28],

    # Inner/small moons
    "metis":      [9.56e16,   127.97e3,   31570.0, 0.06],
    "adrastea":   [1.91e17,   128.98e3,   31490.0, 0.05],
    "amalthea":   [2.08e18,   181.4e3,    26080.0, 0.37],
    "thebe":      [7.77e17,   221.9e3,    23440.0, 1.08],
    "themisto":   [6.9e15,    7.5e6,      8300.0,  43.1],
    "leda":       [1.0e16,    11.16e6,    7350.0,  27.5],
    "ersa":       [8.0e15,    11.7e6,     7200.0,  30.5],
    "pandia":     [9.0e15,    11.7e6,     7200.0,  29.2],
    "dia":        [9.0e15,    12.6e6,     7050.0,  28.2],
    "euporie":    [1.0e16,    19.3e6,     5950.0,  145.8],
    "sponde":     [1.0e16,    24.0e6,     5450.0,  157.2],
    "autonoe":    [1.0e16,    24.3e6,     5400.0,  152.8],
    "callirrhoe": [1.0e16,    24.1e6,     5420.0,  141.8],
}

moon_colors = {
    "jupiter": "orange",
    "io": "gray",
    "europa": "lightblue",
    "ganymede": "brown",
    "callisto": "purple"
}

moon_sizes = {
    "jupiter": 12,
    "io": 3,
    "europa": 3,
    "ganymede": 4,
    "callisto": 4
}
def inclined_orbit(r, v, inclination_deg, theta_deg=0):
    i = np.radians(inclination_deg)
    theta = np.radians(theta_deg)

    x = r * np.cos(theta)
    y = r * np.sin(theta) * np.cos(i)
    z = r * np.sin(theta) * np.sin(i)
    pos = np.array([x, y, z])

    vx = -v * np.sin(theta)
    vy =  v * np.cos(theta) * np.cos(i)
    vz =  v * np.cos(theta) * np.sin(i)
    vel = np.array([vx, vy, vz])

    return pos, vel


def calc_circular_velocity(M, r):
    G = 6.67430e-11
    return np.sqrt(G * M / r)

# Fill in the moon_data dictionary with inclined orbits
for moon, (mass, r, _, inc) in orbital_params.items():
    v = calc_circular_velocity(moon_data["jupiter"][0], r)
    pos, vel = inclined_orbit(r, v, inc)
    moon_data[moon] = [mass, pos, vel]


class Body:
    def __init__(self, name, mass, pos, vel):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=float)         # now 3D
        self.velocity = np.array(vel, dtype=float)    # now 3D
        self.acceleration = np.zeros(3)


bodies = []

# Create all moons and Jupiter
for name, (mass, pos, vel) in moon_data.items():
    body = Body(name, mass, pos, vel)
    bodies.append(body)

    color = moon_colors.get(name, "red")
    size = moon_sizes.get(name, 4)
    body.color = color
    body.marker, = ax.plot([], [], [], 'o', color=color, markersize=size)
    body.trail, = ax.plot([], [], [], '-', lw=0.7, color=color, alpha=0.6)
    body.trail_x = []
    body.trail_y = []
    body.trail_z = []


    # Trail length can vary
    body.trail_length = 500 if name == "jupiter" else 800

# Initialize markers
def init():
    for b in bodies:
        b.marker.set_data_3d([b.pos[0]], [b.pos[1]], [b.pos[2]])
    return [b.marker for b in bodies]

# Gravitational acceleration
def compute_acceleration(bodies):
    G = 6.67430e-11
    jupiter = next(b for b in bodies if b.name == "jupiter")

    for b in bodies:
        if b.name == "jupiter":
            b.acceleration = np.zeros(3)
            continue
        r = jupiter.pos - b.pos
        dist = np.linalg.norm(r)
        if dist == 0:
            b.acceleration = np.zeros(3)
            continue
        b.acceleration = G * jupiter.mass * r / dist**3


# Symplectic velocity verlet step
def velocity_verlet_step(bodies, dt):
    for b in bodies:
        b.pos += b.velocity * dt + 0.5 * b.acceleration * dt**2

    old_acc = [b.acceleration.copy() for b in bodies]
    compute_acceleration(bodies)

    for b, a_old in zip(bodies, old_acc):
        b.velocity += 0.5 * (a_old + b.acceleration) * dt

# Update frame
def update(frame):
    velocity_verlet_step(bodies, dt)
    for b in bodies:
        b.marker.set_data_3d([b.pos[0]], [b.pos[1]], [b.pos[2]])
        b.trail_x.append(b.pos[0])
        b.trail_y.append(b.pos[1])
        b.trail_z.append(b.pos[2])
        if len(b.trail_x) > b.trail_length:
            b.trail_x.pop(0)
            b.trail_y.pop(0)
            b.trail_z.pop(0)
        b.trail.set_data_3d(b.trail_x, b.trail_y, b.trail_z)
    return [b.marker for b in bodies] + [b.trail for b in bodies]

# Start acceleration and animation
compute_acceleration(bodies)
ani = FuncAnimation(fig, update, init_func=init, frames=1000, interval=20)
plt.show()
