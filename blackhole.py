import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants and Parameters
G = 6.67430e-11
c = 3e8
M = 5e30
a = 0.7
r_g = G * M / c**2
r_plus = r_g * (1 + np.sqrt(1 - a**2))  # Outer event horizon

# Accretion Disk Drawing
def accretion_disk(ax, inner=1.2, outer=6, rings=300):
    for r in np.linspace(inner, outer, rings):
        alpha = 1 - (r - inner) / (outer - inner)
        color = (alpha**2, alpha**0.4, 0)
        circle = plt.Circle((0, 0), r * r_g, color=color, fill=True, alpha=0.07, zorder=1)
        ax.add_artist(circle)

# Photon Trajectory
def simulate_photon(r0, phi0, steps, b):
    dt = 0.01
    r = r0
    phi = phi0
    x_vals, y_vals = [], []
    sizes, colors = [], []

    for _ in range(steps):
        if r <= r_plus:
            break
        try:
            dr = np.sqrt(1 - (b**2 / r**2) * (1 - 2 * r_g / r + (a * r_g / r)**2))
        except:
            break
        dphi = b / r**2
        r -= dr * dt
        phi += dphi * dt

        x = r * np.cos(phi)
        y = r * np.sin(phi)
        x_vals.append(x)
        y_vals.append(y)

        dilation = 1 / (1 - r_plus / r)
        sizes.append(min(10, 2.5 * dilation**0.3))

        redshift = min(1, (r_plus / r)**0.5)
        color = (1.0, 1 - redshift, 0)
        colors.append(color)

    return np.array(x_vals), np.array(y_vals), np.array(sizes), colors

# Simulation Parameters
r0 = 12 * r_g
phi0 = np.pi
b = 4.5 * r_g
steps = 4000
x_vals, y_vals, sizes, colors = simulate_photon(r0, phi0, steps, b)
n_frames = len(x_vals)

# Plot Setup
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
limit = 13 * r_g
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_facecolor("black")

# Accretion disk
accretion_disk(ax)

# Visibly exaggerated black hole (to make it appear on the plot)
bh_radius = r_plus * 2.5  # Exaggerated size for visibility
blackhole = plt.Circle((0, 0), bh_radius, color='black', zorder=15)
ax.add_artist(blackhole)

# Photon dot and trail
dot, = ax.plot([], [], 'o', markersize=6, zorder=20)
trail, = ax.plot([], [], color='orange', lw=1.2, alpha=0.8)

def init():
    dot.set_data([], [])
    trail.set_data([], [])
    dot.set_color('orange')
    return dot, trail

# Update Function
def update(frame):
    if frame >= n_frames:
        return dot, trail

    dot.set_data([x_vals[frame]], [y_vals[frame]])
    dot.set_color(colors[frame])
    dot.set_markersize(sizes[frame])
    trail.set_data(x_vals[:frame+1], y_vals[:frame+1])
    return dot, trail


# Animate
ani = FuncAnimation(fig, update, init_func= init, frames=n_frames, interval=10, blit=False)

# Final Touches
plt.title("Kerr Black Hole", color='white')
plt.xlabel("x (m)", color='white')
plt.ylabel("y (m)", color='white')
ax.tick_params(colors='white')
plt.tight_layout()
plt.show()
