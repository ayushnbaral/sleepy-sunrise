import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from moon_dictionary import *
# ===================================
# CHANGE FOR VIEWING DIFFERENT GROUPS
# ===================================
VIEW_GALILEAN = False
VIEW_RETROGRADE = False
VIEW_PROGRADE = True
VIEW_INNER = False

# =========================
# CONSTANTS
# =========================
lim = 4e4 if VIEW_INNER else 4e6
render_speed = 1.03
dt = 10 #--- Default Time Step
inner_dt = 0.01 #--- Innermost Moons fly off if not small enough
w1 = 1 / (2 - 2 ** (1/3))
w2 = - (2 ** (1/3)) / ( 2- 2 ** (1/3))
R_jup = 71492e3  # Jupiter's equatorial radius in meters
J2 = 0.014736  # Jupiter's J₂ value

# =========================
# PLOTTING
# =========================
plt.rcParams['font.family'] = 'cambria'
fig = plt.figure('auto')
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect("auto")
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.view_init(elev=30, azim=120)
fig.patch.set_facecolor('#010b19')
ax.set_facecolor('#010b19')
ax.grid(False)
for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.set_pane_color((1, 1, 1, 0))
    axis._axinfo["grid"]['color'] =  (0, 0, 0, 0)
ax.set_title("Jupiter and its Moons in 3D", color='white')
ax.set_axis_off()

# ==================================
# INITIALIZING JUPITER AND ITS MOONS
# ==================================

def inclined_orbit(r, v, inclination_deg, theta_deg = 0):
    #For 3D orbits
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

def calc_circular_velocity(m, r):
    G = 6.67430e-11
    return np.sqrt(G * m / r)

for moon, (mass, r, _, inc) in orbital_params.items():
    '''Fill moon_data dictionary with inclined orbits'''
    v = calc_circular_velocity(jupiter_data["jupiter"][0], r)
    pos, vel = inclined_orbit(r, v, inc)
    jupiter_data[moon] = [mass, pos, vel]

# =========================
# MARKER
# =========================
class Body:
    def __init__(self, name, mass, pos, vel):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=float)         # now 3D
        self.velocity = np.array(vel, dtype=float)    # now 3D
        self.acceleration = np.zeros(3)
        self.dt = dt

bodies = []
inner = {"metis", "adrastea", "amalthea", "thebe"}
galilean = {"io", "europa", "ganymede", "callisto"}
retrograde = {"euporie", "sponde", "autonoe", "callirrhoe",
              "megaclite", "taygete", "chaldene", "harpalyke",
              "pasiphae", "sinope", "kalyke", "eukelade",
              "philophrosyne", "ananke", "carme", "hermippe",
              "eupheme", "orthosie","thyone", "iocaste"
              }
prograde = {"themisto", "leda", "ersa", "pandia",
            "dia", "carpo", "valetudo", "himalia",
            "elara", "lysithea"
    }

# Groups mapped to their corresponding "view" flags
view_filters = {
    'galilean':   (VIEW_GALILEAN,   galilean),
    'retrograde': (VIEW_RETROGRADE, retrograde),
    'prograde':   (VIEW_PROGRADE,   prograde),
    'inner':      (VIEW_INNER,      inner),
}

for _, (view_flag, group) in view_filters.items():
    '''apply fade to non-selected groups from view_index'''
    if not view_flag:
        for key in group:
            if key in moon_colors:
                moon_colors[key] = 'gray'
                moon_alpha[key] = 0.2

for name, (mass, pos, vel) in jupiter_data.items():
    body = Body(name, mass, pos, vel)
    bodies.append(body)

    color = moon_colors.get(name, "gray")
    alpha = moon_alpha.get(name)
    size = moon_sizes.get(name, 4)
    body.color = color
    body.marker, = ax.plot([], [], [], 'o', color=color, markersize=size, alpha=alpha)
    body.trail, = ax.plot([], [], [], '-', lw=0.7, color=color, alpha=(alpha/1.667))
    body.trail_x = []
    body.trail_y = []
    body.trail_z = []
    body.trail_length = 500 if name == "jupiter" else 300

# =========================
# PHYSICS
# =========================

def compute_acceleration(bodies):
    G = 6.67430e-11
    jupiter = next(b for b in bodies if b.name == "jupiter")
    for b in bodies:
        total_acc = np.zeros(3)
        if b.name == "jupiter":
            b.acceleration = np.zeros(3)
            continue
        r = jupiter.pos - b.pos
        dist = np.linalg.norm(r)
        if dist == 0:
            b.acceleration = np.zeros(3)
            continue
        b.acceleration = G * jupiter.mass * r / dist**3

        total_acc = G * jupiter.mass * r / dist ** 3
        if b.name != "jupiter" and b.name not in inner:
            '''J2 Acceleration on Moons beside Inner Planets'''
            x, y, z = r
            factor = - (3 * G * jupiter.mass * J2 * R_jup ** 2) / (2 * dist ** 5)
            ax_j2 = x * (1 - 5 * z ** 2 / dist ** 2)
            ay_j2 = y * (1 - 5 * z ** 2 / dist ** 2)
            az_j2 = z * (3 - 5 * z ** 2 / dist ** 2)
            j2_acc = factor * np.array([ax_j2, ay_j2, az_j2])
            j2_acc *= 0.1  # try 10% strength
            total_acc += j2_acc
            b.acceleration = total_acc

# Symplectic velocity verlet step
def velocity_verlet_step(bodies, dt):
    for b in bodies:
        '''Yoshida 4th Order Time Integrator for Symplectic Purposes'''
        if b.name.lower() in inner:
            b.pos += b.velocity * inner_dt + 0.5 * b.acceleration * inner_dt ** 2 #--- Inner Moons
        elif b.name.lower() in galilean:
            b.pos += b.velocity * 1000 + 0.5 * b.acceleration * 1000 ** 2 #--- Outer Moons
        else:
            b.pos += b.velocity * dt + 0.5 * b.acceleration * dt**2 #--- Everything Else

    old_acc = [b.acceleration.copy() for b in bodies]
    compute_acceleration(bodies)

    for b, a_old in zip(bodies, old_acc):
        if b.name.lower() in inner:
            b.velocity += 0.5 * (a_old + b.acceleration) * inner_dt #---- Inner Moons
        elif b.name.lower() in galilean:
            b.velocity += 0.5 * (a_old + b.acceleration) * 1000 #--- Outer Moons
        else:
            b.velocity += 0.5 * (a_old + b.acceleration) * dt #--- Everything Else

def view_frame():
    global lim
    '''limit view frame by selected groups'''
    if VIEW_GALILEAN:
        max_lim = 1.5e9
    elif VIEW_RETROGRADE:
        max_lim = 1.6e7
    elif VIEW_PROGRADE:
        max_lim = 1.4e7
    elif VIEW_INNER:
        max_lim = 2e5
    else:
        max_lim = 1
        print("No Groups Selected")
        exit()

    if max_lim < lim or lim >= 2e9: # Limit Frame to only this marker.
        return

    lim *= render_speed
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_zlim(-lim, lim)

# =========================
# ANIMATE
# =========================

def init():
    for b in bodies:
        b.marker.set_data_3d([b.pos[0]], [b.pos[1]], [b.pos[2]])
    return [b.marker for b in bodies]

def update(frame):
    global lim, dt
    for w in [w1, w2, w1]:
        velocity_verlet_step(bodies, dt * w)
    view_frame()

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

compute_acceleration(bodies) #--- Starts Animation
ani = FuncAnimation(fig, update, init_func=init, frames=1000, interval=15)
plt.show()
