import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# --- Planetary Constants --- #
G = 6.6743e-11
c = 299792458
R_ns = 12000
m1 = m2 = 2.78e30
init_dist = 1000e3

# --- Conditions --- #
lim = init_dist * 0.7
merger_triggered = False
explosion_frame = 0

# --- Constants --- #
PM_CONST = (64 / 5) * (G ** 3 * (m1 * m2) ** 2 / (m1 + m2)) / c ** 5
v = np.sqrt(G * (m1 + m2) / init_dist) / 2
T = 3.1415 * init_dist / v * 1
pointsPerPeriod = 1000
dt = T / pointsPerPeriod * 2
v1 = np.array([0, v], dtype=float)
v2 = np.array([0, -v], dtype=float)

# --- Positions --- #
start_color = np.array([1.0, 1.0, 1.0])
end_color   = np.array([0.9, 0.2, 0.2])
trail1_x, trail1_y = [], []
trail2_x, trail2_y = [], []
pos1 = np.array([-init_dist / 2, 0], dtype=float)
pos2 = np.array([init_dist / 2, 0], dtype=float)

# --- Plot --- #
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
plt.scatter([0], [0], color='white', marker='x', label="Center of Mass")
pos1_dot, = ax.plot([], [], marker='o', color='#703be7', ms=16, label='Star 1', zorder=2)
pos2_dot, = ax.plot([], [], marker='o', color='#703be7', ms=16, label='Star 2', zorder=2)
merger = Circle((0, 0), 1, zorder=3)
ax.add_patch(merger)
trail1_line, = ax.plot([], [], ls = '-', color ='r', lw=0.75, zorder=1)
trail2_line, = ax.plot([], [], ls = '-', color ='w', lw=0.75, zorder = 1)
fig.set_facecolor('#010b19')
ax.set_facecolor('#010b19')
ax.tick_params(axis='x', colors='#010b19')
ax.tick_params(axis='y', colors='#010b19')
for spine in ax.spines.values():
    spine.set_color('white')

def compute_accelerations(pos1, pos2):
    r_vec = pos2 - pos1
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag
    force_mag = G * m1 * m2 / r_mag ** 2 # Force formula
    a1 = force_mag / m1 * r_hat
    a2 = -force_mag / m2 * r_hat # Opposite to attract towards each other
    return a1, a2

a1, a2 = compute_accelerations(pos1, pos2)

def verlet_integration(pos1, pos2, a1, a2, v1, v2):
    pos1_new = pos1 + v1 * dt + 0.5 * a1 * dt ** 2 # Velocity Verlet
    pos2_new = pos2 + v2 * dt + 0.5 * a2 * dt ** 2
    a1_new, a2_new = compute_accelerations(pos1_new, pos2_new)
    v1_new = v1 + 0.5 * (a1 + a1_new) * dt
    v2_new = v2 + 0.5 * (a2 + a2_new) * dt
    return pos1_new, pos2_new, v1_new, v2_new, a1_new, a2_new # Setting new positions

def peters_mathews(pos1, pos2, v1, v2): # Orbital Decay
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    delta_r = -5e3 * (PM_CONST / (r ** 3) * dt)
    r_new = r + delta_r
    r_hat = r_vec / r
    if r_new <= R_ns or r_new <= 0:
        global merger_triggered
        merger_triggered = True
        return pos1, pos2, v1, v2
    pos1_new = pos1 - 0.5 * (r_new - r) * r_hat
    pos2_new = pos2 + 0.5 * (r_new - r) * r_hat
    v_mag = np.sqrt(G * (m1 + m2) / r_new) / 2
    tangential_dir = np.array([-r_hat[1], r_hat[0]])
    v1_new = v_mag * tangential_dir
    v2_new = -v1_new
    return pos1_new, pos2_new, v1_new, v2_new

def init():
    pos1_dot.set_data([], [])
    pos2_dot.set_data([], [])
    trail1_line.set_data([], [])
    trail2_line.set_data([], [])
    merger.set_visible(False)
    merger.set_radius(1)
    return pos1_dot, pos2_dot, trail1_line, trail2_line

def update(frame):
    global pos1, pos2, v1, v2, a1, a2
    pos1, pos2, v1, v2, a1, a2 = verlet_integration(pos1, pos2, a1, a2, v1, v2)
    pos1, pos2, v1, v2 = peters_mathews(pos1, pos2, v1, v2)

    # Update trail data
    trail1_x.append(pos1[0])
    trail1_y.append(pos1[1])
    trail2_x.append(pos2[0])
    trail2_y.append(pos2[1])

    # Update plot data
    pos1_dot.set_data([pos1[0]], [pos1[1]])
    pos2_dot.set_data([pos2[0]], [pos2[1]])
    trail1_line.set_data(trail1_x, trail1_y)
    trail2_line.set_data(trail2_x, trail2_y)

    global explosion_frame

    if merger_triggered:
        pos1_dot.set_data([], [])
        pos2_dot.set_data([], [])
        trail1_line.set_data([], [])
        trail2_line.set_data([], [])

        merger.set_visible(True)
        merger.set_radius(50000 * np.sqrt(explosion_frame + 1))
        t = explosion_frame / 50
        t = min(t, 1.0)
        color = (1 - t) * start_color + t * end_color
        merger.set_facecolor(color)
        merger.set_alpha(1.0 - t)
        explosion_frame += 1
        if explosion_frame > 100:
            ani.event_source.stop()
        return merger, trail1_line, trail2_line
    return pos1_dot, pos2_dot, trail1_line, trail2_line, merger

ani = FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=5000,
    interval=14,
    blit=True
)

plt.show()
