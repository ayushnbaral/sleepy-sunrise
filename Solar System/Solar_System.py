import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

lim = 32 * 1.496e11
zoom = False

plt.rcParams['font.family'] = 'cambria'
fig, ax = plt.subplots()
ax.set_aspect('equal')
fig.set_facecolor('#010b19')
ax.set_facecolor('#010b19')

# -- Constants -- #
dt = 86400
planet_data = {
    "sun":      [1.989e30,     [0.0, 0.0],           [0.0, 0.0]],
    "mercury":  [3.301e23,     [5.79e10, 0.0],       [0.0, 47890.0]],
    "venus":    [4.867e24,     [1.082e11, 0.0],      [0.0, 35020.0]],
    "earth":    [5.972e24,     [1.496e11, 0.0],      [0.0, 29780.0]],
    "mars":     [6.417e23,     [2.279e11, 0.0],      [0.0, 24130.0]],
    "jupiter":  [1.899e27,     [7.785e11, 0.0],      [0.0, 13070.0]],
    "saturn":   [5.685e26,     [1.433e12, 0.0],      [0.0, 9680.0]],
    "uranus":   [8.682e25,     [2.877e12, 0.0],      [0.0, 6810.0]],
    "neptune":  [1.024e26,     [4.503e12, 0.0],      [0.0, 5430.0]]
}
planet_colors = {
    "sun": "yellow",
    "mercury": "gray",
    "venus": "orange",
    "earth": "blue",
    "mars": "red",
    "jupiter": "brown",
    "saturn": "gold",
    "uranus": "cyan",
    "neptune": "violet"
}

planet_sizes = {
    "sun": 22,        # ~109x Earth's size → scaled down to stay visible
    "mercury": 2,     # 0.38x Earth
    "venus": 5,       # 0.95x Earth
    "earth": 5,
    "mars": 3,        # 0.53x Earth
    "jupiter": 11,    # 11x Earth
    "saturn": 10,     # 9x Earth
    "uranus": 6,      # 4x Earth
    "neptune": 6      # 3.9x Earth
}

if not zoom:
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_title("Solar System (time = 10 days)", color='white')
    planet_sizes.update({"sun":1})
    dt = 864000
else:
    ax.set_xlim(-lim / 10, lim / 10)
    ax.set_ylim(-lim / 10, lim / 10)
    del planet_data["jupiter"], planet_data["saturn"], planet_data["uranus"], planet_data["neptune"]
    ax.set_title("Inner Planets (time = 1 day)", color='white')

class Planet:
    def __init__(self, name, mass, pos, vel):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(vel, dtype=float)
        self.acceleration = np.zeros(2)

planets = []



for name, (mass, pos, vel) in planet_data.items():
    planet = Planet(name, mass, pos, vel)
    planets.append(planet)
    color = planet_colors.get(name, "white")
    size = planet_sizes.get(name, 4)
    planet.color = color
    planet.marker, = ax.plot([], [], 'o', color=color, markersize=size)
    planet.trail, = ax.plot([], [], '-', lw=0.7, color=color, alpha=0.6)
    planet.trail_x = []
    planet.trail_y = []

    # Assign trail length per planet
    if name in {"mercury", "venus", "earth", "mars"}:
        planet.trail_length = 250
    else:
        planet.trail_length = 700

def init():
    for p in planets:
        p.marker.set_data([p.pos[0]], [p.pos[1]])
    return [p.marker for p in planets]


def compute_acceleration(planets):
    G = 6.67430e-11

    for p in planets:
        total_acceleration = np.zeros(2)

        for other in planets:
            if p is other:
                continue

            r = other.pos - p.pos
            dist = np.linalg.norm(r)
            if dist == 0:
                continue

            force_dir = r / dist
            acc = G * other.mass / dist ** 2
            total_acceleration += acc * force_dir
        p.acceleration = total_acceleration


# noinspection SpellCheckingInspection
def velocity_verlet_step(planets, dt):

    for p in planets:
        p.pos += p.velocity * dt + 0.5 * p.acceleration * dt ** 2

    old_accelerations = [p.acceleration.copy() for p in planets]
    compute_acceleration(planets)

    for p, a_old in zip(planets, old_accelerations):
        p.velocity += 0.5 * (a_old + p.acceleration) * dt

compute_acceleration(planets)

def update(frame):
    velocity_verlet_step(planets, dt)

    for p in planets:
        p.marker.set_data([p.pos[0]], [p.pos[1]])
        p.trail_x.append(p.pos[0])
        p.trail_y.append(p.pos[1])
        if len(p.trail_x) > p.trail_length:
            p.trail_x.pop(0)
            p.trail_y.pop(0)
        p.trail.set_data(p.trail_x, p.trail_y)
    return [p.marker for p in planets] + [p.trail for p in planets]



ani = FuncAnimation(fig, update, init_func=init, frames=1000, interval=15, blit=True)
plt.show()
