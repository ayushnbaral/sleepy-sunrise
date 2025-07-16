import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
AU = 1.496e11  # meters
year = 365.25 * 24 * 3600  # seconds in a year
G = 6.67430e-11
M_sun = 1.989e30

# Orbital parameters: [semi-major axis (AU), eccentricity, period (years), color, size]
planets = {
    "Mercury": [0.39, 0.206, 0.24, 'gray', 3],
    "Venus":   [0.72, 0.007, 0.62, 'orange', 5],
    "Earth":   [1.00, 0.017, 1.00, 'blue', 6],
    "Mars":    [1.52, 0.093, 1.88, 'red', 4],
    "Jupiter": [5.20, 0.049, 11.86, 'gold', 7],
    "Saturn":  [9.58, 0.056, 29.46, 'khaki', 6],
    "Uranus":  [19.2, 0.046, 84.01, 'lightblue', 5],
    "Neptune": [30.1, 0.010, 164.8, 'purple', 5]
}

# Precompute orbit paths (elliptical) for drawing
theta = np.linspace(0, 2 * np.pi, 500)
orbits = {}
for name, (a, e, _, _, _) in planets.items():
    r = a * (1 - e**2) / (1 + e * np.cos(theta))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    orbits[name] = (x, y)

# Initialize figure
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_facecolor('black')
fig.set_facecolor('black')
ax.set_xlim(-35, 35)
ax.set_ylim(-35, 35)
ax.set_title("Solar System Simulation (Elliptical Orbits)", color='white')
ax.tick_params(colors='white')

# Draw orbits
for name, (x, y) in orbits.items():
    ax.plot(x, y, color='white', linestyle='--', linewidth=0.5)

# Plot Sun
sun_dot, = ax.plot(0, 0, 'yo', markersize=10, label='Sun')

# Initialize planet dots and trails
planet_dots = {}
planet_trails = {}
trail_data = {}

for name, (_, _, _, color, size) in planets.items():
    dot, = ax.plot([], [], 'o', color=color, markersize=size, label=name)
    trail, = ax.plot([], [], color=color, linewidth=1, alpha=0.5)
    planet_dots[name] = dot
    planet_trails[name] = trail
    trail_data[name] = ([], [])

# Time management
t = 0
dt = 20 * 24 * 3600  #  days per frame

'''
scale_factors = {
    'Mercury': 4,
    'Venus': 3,
    'Earth': 2.5,
    'Mars': 2,
    'Jupiter': 1,
    'Saturn': 1,
    'Uranus': 1,
    'Neptune': 1
}
'''

# Animation update
def animate(frame):
    global t
    t += dt

    for name, (a, e, T, color, size) in planets.items():
        # Mean motion
        n = 2 * np.pi / (T * year)

        # Mean anomaly
        M = n * t

        # Solve Kepler's Equation: M = E - e*sin(E)
        E = M
        for _ in range(5):  # Newton-Raphson
            E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))

        # True anomaly
        theta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                               np.sqrt(1 - e) * np.cos(E / 2))

        # Distance from Sun
        r = a * (1 - e * np.cos(E))

        # Position in Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        # Update planet position
        planet_dots[name].set_data([x],[y])

        # Update trail
        trail_x, trail_y = trail_data[name]
        trail_x.append(x)
        trail_y.append(y)

        # Limit trail length
        max_len = 100
        if len(trail_x) > max_len:
            trail_x.pop(0)
            trail_y.pop(0)

        planet_trails[name].set_data(trail_x, trail_y)

    return list(planet_dots.values()) + list(planet_trails.values()) + [sun_dot]

# Animate
ani = FuncAnimation(fig, animate, frames=5000, interval=30, blit=True)
plt.legend(loc='upper right', facecolor='black', labelcolor='white')
plt.show()
