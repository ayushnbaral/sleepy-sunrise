import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# Constants
G = 6.67430e-11
c = 3e8
M = 5e30
a = 0.7
r_g = G * M / c**2
r_plus = r_g * (1 + np.sqrt(1 - a**2))

# Time dilation factor
def get_time_dilation_factor(r):
    return 1 / np.sqrt(np.maximum(1e-6, 1 - r_plus / (r * r_g)))

# Photon
def simulate_photon(r0, phi0, b, steps=3000):
    E = 6.0
    L = b * E

    def geodesic(_, y):
        r, phi, pr = y
        delta = r**2 - 2*r + a**2
        R = E**2 * r**4 + (a**2 * E**2 - L**2) * r**2 + 2*(a*E - L)**2 * r - a**2 * (L - a*E)**2
        if delta <= 0 or R < 0:
            return [0, 0, 0]
        dr = pr
        dphi = (2*a*r*E + (r**2 + a**2 - 2*r)*L/delta) / r**2
        dpr = -0.5 * (4*E**2*r**3 + 2*(a**2*E**2 - L**2)*r +
                      2*(a*E - L)**2 - 2*a**2*(L - a*E)**2/r) / r**4
        return [dr, dphi, dpr]

    pr0 = -np.sqrt(max(E**2 * r0**4 + (a**2 * E**2 - L**2) * r0**2 +
                       2*(a*E - L)**2 * r0 - a**2*(L - a*E)**2, 0)) / r0**2
    y0 = [r0, phi0, pr0]

    sol = solve_ivp(geodesic, (0, 50), y0, t_eval=np.linspace(0, 50, steps), rtol=1e-8)
    r_vals, phi_vals = sol.y[0], sol.y[1]
    mask = r_vals > r_plus / r_g

    x = r_vals[mask] * np.cos(phi_vals[mask]) * r_g
    y = r_vals[mask] * np.sin(phi_vals[mask]) * r_g
    dist = r_vals[mask] * r_g
    proximity = np.maximum(1e-6, dist - r_plus)
    stretch = np.clip(1 + 100 / (proximity + 1e-6), 1, 200)
    return x, y, stretch

# Massive particle
def simulate_massive_particle(r0, phi0, b, steps=3000):
    E = 5.0  # Faster initial speed
    L = b * E

    def geodesic(_, y):
        r, phi, pr = y
        delta = r**2 - 2*r + a**2
        V_eff = E**2 - (1 - 2/r)*(1 + L**2 / r**2)
        if delta <= 0 or V_eff < 0:
            return [0, 0, 0]
        dr = pr
        dphi = L / r**2
        dpr = -0.5 * (2*(1 - 2/r)*L**2/r**3 - 4/r**2)
        return [dr, dphi, dpr]

    pr0 = -np.sqrt(max(E**2 - (1 - 2/r0)*(1 + L**2 / r0**2), 0))
    y0 = [r0, phi0, pr0]

    sol = solve_ivp(geodesic, (0, 50), y0, t_eval=np.linspace(0, 50, steps), rtol=1e-8)
    r_vals, phi_vals = sol.y[0], sol.y[1]
    mask = r_vals > r_plus / r_g

    x = r_vals[mask] * np.cos(phi_vals[mask]) * r_g
    y = r_vals[mask] * np.sin(phi_vals[mask]) * r_g
    dist = r_vals[mask] * r_g
    proximity = np.maximum(1e-6, dist - r_plus)
    stretch = np.clip(1 + 100 / (proximity + 1e-6), 1, 200)
    return x, y, stretch

# Run
x_photon, y_photon, stretch_photon = simulate_photon(14, np.pi, 3.0)
x_massive, y_massive, stretch_massive = simulate_massive_particle(14, 0, 2.7)

# Frame count: stop after spaghettification
max_stretch_idx = max(np.argmax(stretch_massive), np.argmax(stretch_photon))
n_frames = min(len(stretch_massive), len(stretch_photon), max_stretch_idx + 130)

# Plot
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal')
ax.set_xlim(-12 * r_g, 12 * r_g)
ax.set_ylim(-12 * r_g, 12 * r_g)
ax.set_facecolor("black")

def accretion_disk(ax, inner=1.3, outer=6, rings=300):
    for r in np.linspace(inner, outer, rings):
        alpha = 1 - (r - inner) / (outer - inner)
        color = (alpha**2, alpha**0.4, 0)
        circle = plt.Circle((0, 0), r * r_g, color=color, fill=True, alpha=0.07, zorder=1)
        ax.add_artist(circle)

accretion_disk(ax)

blackhole = plt.Circle((0, 0), r_plus * 1.5, color='black', zorder=5)
ax.add_artist(blackhole)

# Trails and objects
trail_len = 100
trail_photon, = ax.plot([], [], color='orange', lw=1.2)
dot_photon = plt.Rectangle((0, 0), 5, 5, color='orange', zorder=50)
ax.add_patch(dot_photon)

trail_massive, = ax.plot([], [], color='violet', lw=1.2)
dot_massive = plt.Rectangle((0, 0), 5, 5, color='violet', zorder=50)
ax.add_patch(dot_massive)

def init():
    trail_photon.set_data([], [])
    trail_massive.set_data([], [])
    dot_photon.set_xy((-100, -100))
    dot_massive.set_xy((-100, -100))
    return trail_photon, dot_photon, trail_massive, dot_massive

def update(frame):
    # Trails
    i0 = max(0, frame - trail_len)
    trail_photon.set_data(x_photon[i0:frame+1], y_photon[i0:frame+1])
    trail_massive.set_data(x_massive[i0:frame+1], y_massive[i0:frame+1])

    # Photon shape
    elong_ph = stretch_photon[frame]
    dot_photon.set_width(5 / elong_ph)
    dot_photon.set_height(5 * elong_ph)
    dot_photon.set_xy((x_photon[frame] - 2.5 / elong_ph, y_photon[frame] - 2.5 * elong_ph))

    # Massive particle shape
    elong_mp = stretch_massive[frame]
    dot_massive.set_width(5 / elong_mp)
    dot_massive.set_height(5 * elong_mp)
    dot_massive.set_xy((x_massive[frame] - 2.5 / elong_mp, y_massive[frame] - 2.5 * elong_mp))

    # Visual time dilation
    r_current = np.sqrt(x_massive[frame]**2 + y_massive[frame]**2) / r_g
    dilation = get_time_dilation_factor(r_current)
    ani.event_source.interval = min(60, 15 * dilation)

    return trail_photon, dot_photon, trail_massive, dot_massive

ani = FuncAnimation(fig, update, init_func=init, frames=n_frames, interval=15, blit=False)

plt.title("Photon & Spaghettifying Particle Near Kerr Black Hole", color='white')
ax.tick_params(colors='white')
plt.tight_layout()
plt.show()
