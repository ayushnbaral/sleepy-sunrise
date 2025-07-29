import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# =========================
# PHYSICAL CONSTANTS
# =========================
G = 6.6743e-11         # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458          # Speed of light (m/s)
R_ns = 12000           # Approximate radius of a neutron star (m)
m1 = 2.78e30           # Mass of neutron star 1 (kg)
m2 = 2.78e30           # Mass of neutron star 2 (kg)

# Derived quantities
init_dist = 1e5        # Initial separation (m)
M = m1 + m2            # Total mass
mu = (m1 * m2) / M     # Reduced mass
eta = mu / M           # Symmetric mass ratio

# =========================
# SIMULATION PARAMETERS
# =========================
lim = init_dist * 1  # Initial plot limit
merger_triggered = False
explosion_frame = 0

# Orbital parameters
v = 0.98 * np.sqrt(G * M / init_dist) * m2 / M  # Initial orbital speed (reduced)
T = np.pi * init_dist / v                       # Orbital period
dt = (T / 1000) * 25                           # Timestep

# =========================
# VISUAL PARAMETERS
# =========================
start_color         = np.array([1.0, 1.0, 1.0])  # Merger start (white)
end_color           = np.array([0.9, 0.2, 0.2])  # Merger end (red)
start_ejecta_color  = np.array([1.0, 0.27, 0.0]) # Hot ejecta (orange)
end_ejecta_color    = np.array([1.0, 0.41, 0.71])# Cooler ejecta (pink)

# =========================
# INITIAL CONDITIONS
# =========================
r1 = np.array([-init_dist / 2, 0], dtype=float)
r2 = np.array([ init_dist / 2, 0], dtype=float)
v1 = np.array([0,  v], dtype=float)
v2 = np.array([0, -v], dtype=float)

trail1_x, trail1_y = [], []
trail2_x, trail2_y = [], []

# =========================
# EJECTA INITIALIZATION
# =========================
Num_ejecta = 150
ejecta_positions = []
ejecta_velocities = []

# =========================
# PLOTTING SETUP
# =========================
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
fig.set_facecolor('#010b19')
ax.set_facecolor('#010b19')
ax.set_title("Kilonova Simulation", color='white')
ax.tick_params(axis='x', colors='#010b19')
ax.tick_params(axis='y', colors='#010b19')

# Plot: static features
plt.rcParams['font.family'] = 'Franklin Gothic Book'
plt.scatter([0], [0], color='white', marker='x', label="Center of Mass")

# Plot: dynamic features
pos1_dot, = ax.plot([], [], 'o', color='#703be7', ms=17, label='Star 1', zorder=2)
pos2_dot, = ax.plot([], [], 'o', color='#703be7', ms=17, label='Star 2', zorder=2)
trail1_line, = ax.plot([], [], '-', color='r', lw=0.75, zorder=1)
trail2_line, = ax.plot([], [], '-', color='w', lw=0.75, zorder=1)
ejecta_scatter = ax.scatter([], [], s=5, alpha=0.8, zorder=2)

# Merger visuals
merger = Circle((0, 0), 1, visible=False, zorder=3)
shockwave = Circle((0, 0), radius=1, fc='none', ec='white', lw=1.5, alpha=0.5, visible=False)
ax.add_patch(merger)
ax.add_patch(shockwave)

# Glowing effect behind stars
glow1_dot, = ax.plot([], [], 'o', color='#703be7', ms=30, alpha=0.15, zorder=1)
glow2_dot, = ax.plot([], [], 'o', color='#703be7', ms=30, alpha=0.15, zorder=1)

# White borderlines
for spine in ax.spines.values():
    spine.set_color('white')

# =========================
# PHYSICS CALCULATIONS
# =========================
def relative_vectors(r1, r2, v1, v2):
    r_vec = r2 - r1
    v_vec = v2 - v1
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    n_hat = r_vec / r
    return r, v, n_hat, r_vec, v_vec

def acceleration_newton(r, n_hat):
    return - (G * M) / r**2 * n_hat

def acceleration_1PN(r, v, n_hat, v_vec):
    v_dot_n = np.dot(v_vec, n_hat)
    term1 = (1 + 3 * eta) * v**2
    term2 = -2 * (2 + eta) * (G * M / r)
    term3 = -1.5 * eta * v_dot_n**2
    return - (G * M) / r**2 * (n_hat * (term1 + term2 + term3) - 2 * (2 - eta) * v_dot_n * v_vec) / c**2

def acceleration_2_5PN(r, v, n_hat, v_vec):
    v_dot_n = np.dot(v_vec, n_hat)
    coeff = (8/5) * eta * G**2 * M**2 / (c**5 * r**3)
    return coeff * (n_hat * v_dot_n * (18 * v**2 + (2/3) * (G * M / r) - 25 * v_dot_n**2)
                    - v_vec * (6 * v**2 - 2 * (G * M / r) - 15 * v_dot_n**2))

def compute_accelerations(r1, r2, v1, v2):
    r, v, n_hat, r_vec, v_vec = relative_vectors(r1, r2, v1, v2)
    a_newton = acceleration_newton(r, n_hat)
    a_1pn = acceleration_1PN(r, v, n_hat, v_vec)
    a_2_5pn = acceleration_2_5PN(r, v, n_hat, v_vec)
    a_total = a_newton + a_1pn + a_2_5pn
    a1 = -(m2 / M) * a_total
    a2 =  (m1 / M) * a_total
    return a1, a2

def rk4_step(r1, r2, v1, v2, dt):
    """4th order Runge-Kutta integrator with post-Newtonian corrections."""
    global merger_triggered

    if np.linalg.norm(r2 - r1) < 2 * R_ns:
        merger_triggered = True
        return r1, r2, v1, v2

    a1_k1, a2_k1 = compute_accelerations(r1, r2, v1, v2)
    r1_k2 = r1 + 0.5 * dt * v1
    r2_k2 = r2 + 0.5 * dt * v2
    v1_k2 = v1 + 0.5 * dt * a1_k1
    v2_k2 = v2 + 0.5 * dt * a2_k1
    a1_k2, a2_k2 = compute_accelerations(r1_k2, r2_k2, v1_k2, v2_k2)

    r1_k3 = r1 + 0.5 * dt * v1_k2
    r2_k3 = r2 + 0.5 * dt * v2_k2
    v1_k3 = v1 + 0.5 * dt * a1_k2
    v2_k3 = v2 + 0.5 * dt * a2_k2
    a1_k3, a2_k3 = compute_accelerations(r1_k3, r2_k3, v1_k3, v2_k3)

    r1_k4 = r1 + dt * v1_k3
    r2_k4 = r2 + dt * v2_k3
    v1_k4 = v1 + dt * a1_k3
    v2_k4 = v2 + dt * a2_k3
    a1_k4, a2_k4 = compute_accelerations(r1_k4, r2_k4, v1_k4, v2_k4)

    r1_new = r1 + (dt / 6) * (v1 + 2 * v1_k2 + 2 * v1_k3 + v1_k4)
    r2_new = r2 + (dt / 6) * (v2 + 2 * v2_k2 + 2 * v2_k3 + v2_k4)
    v1_new = v1 + (dt / 6) * (a1_k1 + 2 * a1_k2 + 2 * a1_k3 + a1_k4)
    v2_new = v2 + (dt / 6) * (a2_k1 + 2 * a2_k2 + 2 * a2_k3 + a2_k4)
    return r1_new, r2_new, v1_new, v2_new

# =========================
# ANIMATION FUNCTIONS
# =========================
def init():
    pos1_dot.set_data([], [])
    pos2_dot.set_data([], [])
    trail1_line.set_data([], [])
    trail2_line.set_data([], [])
    merger.set_visible(False)
    ejecta_scatter.set_offsets(np.empty((0, 2)))
    ejecta_scatter.set_alpha(0.0)
    glow1_dot.set_data([], [])
    glow2_dot.set_data([], [])
    return pos1_dot, pos2_dot, trail1_line, trail2_line, ejecta_scatter, glow1_dot, glow2_dot

def update(frame):
    global r1, r2, v1, v2, explosion_frame

    r1, r2, v1, v2 = rk4_step(r1, r2, v1, v2, dt)

    if merger_triggered:
        pos1_dot.set_data([], [])
        pos2_dot.set_data([], [])
        trail1_line.set_data([], [])
        trail2_line.set_data([], [])
        glow1_dot.set_data([], [])
        glow2_dot.set_data([], [])

        merger.set_visible(True)
        merger.set_radius(400000 * np.sqrt(explosion_frame + 1))

        t = min(explosion_frame / 50, 1.0)
        merger.set_facecolor((1 - t) * start_color + t * end_color)
        merger.set_alpha(1.0 - t)

        shockwave.set_visible(True)
        shockwave.set_radius(300000 * np.sqrt(explosion_frame + 1))
        shockwave.set_alpha(max(0.0, 1.0 - explosion_frame / 100))

        if explosion_frame == 0:
            ax.set_xlim(-lim * 30, lim * 30)
            ax.set_ylim(-lim * 30, lim * 30)
            ejecta_positions.clear()
            ejecta_velocities.clear()
            v_eq, v_pol = 0.05 * c, 0.2 * c

            for _ in range(Num_ejecta):
                angle = np.random.uniform(0, 2 * np.pi)
                v_theta = v_eq + (v_pol - v_eq) * np.cos(angle)**2
                vx, vy = v_theta * np.cos(angle), v_theta * np.sin(angle)
                ejecta_velocities.append(np.array([vx, vy]))
                ejecta_positions.append(np.array([0.0, 0.0]))

        for i in range(Num_ejecta):
            ejecta_positions[i] += ejecta_velocities[i] * (dt * 4)

        ejecta_scatter.set_offsets(np.array(ejecta_positions))

        t = min(explosion_frame / 100, 1.0)
        current_color = (1 - t) * start_ejecta_color + t * end_ejecta_color
        ejecta_scatter.set_facecolor(np.tile(current_color, (Num_ejecta, 1)))
        ejecta_scatter.set_alpha(max(0.0, 1.0 - explosion_frame / 100))

        explosion_frame += 1
        if explosion_frame > 100:
            ani.event_source.stop()

        return merger, trail1_line, trail2_line, ejecta_scatter, glow1_dot, glow2_dot, shockwave

    # Binary still orbiting
    trail1_x.append(r1[0])
    trail1_y.append(r1[1])
    trail2_x.append(r2[0])
    trail2_y.append(r2[1])
    if len(trail1_x) > 50:
        trail1_x.pop(0)
        trail1_y.pop(0)
        trail2_x.pop(0)
        trail2_y.pop(0)

    pos1_dot.set_data([r1[0]], [r1[1]])
    pos2_dot.set_data([r2[0]], [r2[1]])
    trail1_line.set_data(trail1_x, trail1_y)
    trail2_line.set_data(trail2_x, trail2_y)
    glow1_dot.set_data([r1[0]], [r1[1]])
    glow2_dot.set_data([r2[0]], [r2[1]])

    return pos1_dot, pos2_dot, trail1_line, trail2_line, merger, glow1_dot, glow2_dot, ejecta_scatter

# =========================
# ANIMATION LAUNCH
# =========================
ani = FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=5000,
    interval=15,
    blit=True
)

plt.show()
