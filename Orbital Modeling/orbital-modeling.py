import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# Constants
earth_radius = 60000
moon_radius = 31200
moon_distance = 384400
orbital_period = 27.3 * 24 * 60 * 60  # seconds in one orbit

fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.set_xlim(-moon_distance - moon_radius - 10000, moon_distance + moon_radius + 10000)
ax.set_ylim(-moon_distance - moon_radius - 8000, moon_distance + moon_radius + 10000)
ax.set_xlabel('Distance (km)', color='white')
ax.set_ylabel('Distance (km)', color='white')
ax.set_title('Moon Orbit', color='white')
fig.set_facecolor('#000015')
ax.set_facecolor('#000015')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Earth glow layers
for i in range(1, 6):
    glow = plt.Circle(
        (0, 0),
        earth_radius + i * 3000,
        color='#ADD8E6',
        alpha=0.05 * (6 - i),
        zorder=2
    )
    ax.add_patch(glow)

earth_circle = plt.Circle((0, 0), earth_radius, color='#ADD8E6', label='Earth', zorder=3)
ax.add_patch(earth_circle)

moon_circle = plt.Circle((moon_distance, 0), moon_radius, color='#F6F1D5', label='Moon', zorder=4)
ax.add_patch(moon_circle)

moon_trail, = ax.plot([], [], color='white', alpha=1, linewidth=2.5, zorder=1)

# Orbit path (static)
orbit_theta = np.linspace(0, 2 * np.pi, 300)
orbit_x = moon_distance * np.cos(orbit_theta)
orbit_y = moon_distance * np.sin(orbit_theta)
moon_orbit, = ax.plot(orbit_x, orbit_y, color='darkgray', linestyle='--', label='Moon Orbit', zorder=0)

# Moon glow layers
moon_glow_layers = []
for i in range(1, 6):
    glow = plt.Circle(
        (moon_distance, 0),
        moon_radius + i * 3000,
        color='#F6F1D5',
        alpha=0.05 * (6 - i),
        zorder=3
    )
    moon_glow_layers.append(glow)
    ax.add_patch(glow)

# Use deque for trail
trail_length = 80
trail_points_x = deque(maxlen=trail_length)
trail_points_y = deque(maxlen=trail_length)

speed_multiplier = 2000  # slower for smoother movement
interval = 10  # milliseconds between frames (increase smoothness)

def frame_generator():
    i = 0
    while True:
        yield i
        i += 1

def init():
    moon_trail.set_data([], [])
    for glow in moon_glow_layers:
        glow.set_center((moon_distance, 0))
    moon_circle.set_center((moon_distance, 0))
    return [moon_circle, moon_trail, *moon_glow_layers]

def update(frame):
    angle = 2 * np.pi * ((frame * speed_multiplier) % orbital_period) / orbital_period
    moon_x = moon_distance * np.cos(angle)
    moon_y = moon_distance * np.sin(angle)

    moon_circle.set_center((moon_x, moon_y))

    trail_points_x.append(moon_x)
    trail_points_y.append(moon_y)
    moon_trail.set_data(trail_points_x, trail_points_y)

    for glow in moon_glow_layers:
        glow.set_center((moon_x, moon_y))

    return [moon_circle, moon_trail, *moon_glow_layers]

ani = FuncAnimation(
    fig, update,
    frames=frame_generator(),
    init_func=init,
    interval=interval,
    blit=True,
    cache_frame_data=False  # <-- This suppresses the warning for infinite frames
)

plt.show()
