# Kilonova
This simulation models the binary pulsar of two neutron stars and their merger.
[Kilonova](https://en.wikipedia.org/wiki/Kilonova), and [Binary Pulsars](https://en.wikipedia.org/wiki/Binary_pulsar) are a very interesting topic, as many elements are released when a kilonova occurs: gold, uranium, and platinum.  

## Problem

We wanted to model a binary pulsar of two neutron stars that ended in a kilonova with decaying orbit using gravitational forces and general relativity.

## Approach

Initially, we started with [Velocity Verlet](https://www.youtube.com/watch?v=1bwsy26x24Q) as our integrator that took in values from a compute_accelerations program. 
```
def compute_accelerations(pos1, pos2):
    r_vec = pos2 - pos1
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag
    force_mag = G * m1 * m2 / r_mag ** 2 # Force formula
    a1 = force_mag / m1 * r_hat
    a2 = -force_mag / m2 * r_hat # Opposite to attract towards each other
    return a1, a2
```
```
def verlet_integration(pos1, pos2, a1, a2, v1, v2):
    pos1_new = pos1 + v1 * dt + 0.5 * a1 * dt ** 2 # Velocity Verlet
    pos2_new = pos2 + v2 * dt + 0.5 * a2 * dt ** 2
    a1_new, a2_new = compute_accelerations(pos1_new, pos2_new)
    v1_new = v1 + 0.5 * (a1 + a1_new) * dt
    v2_new = v2 + 0.5 * (a2 + a2_new) * dt
    return pos1_new, pos2_new, v1_new, v2_new, a1_new, a2_new # Setting new positions
```
After this integration method, we used the [Peters Mathews Formula](https://ui.adsabs.harvard.edu/abs/1996NCimB.111..631P/abstract) to simulate artificial decay at a 2.5 Post Newtonian Order. You can find this formula [here](https://www.roma1.infn.it/teongrav/VESF/SCHOOL2013_WEBSITE/LECTURES/VESFnotes_Blanchet.pdf) on page 12. 
```
def peters_mathews(pos1, pos2, v1, v2):
    r_vec = pos2 - pos1
    r = np.linalg.norm(r_vec)
    delta_r = -2.5e4 * (PM_CONST / (r ** 3) * dt) #Change the Constant to reflect speed
    r_new = r + delta_r
    r_hat = r_vec / r

    if r_new <= R_ns or r_new <= 0:
        global merger_triggered
        merger_triggered = True
        return pos1, pos2, v1, v2

    pos1_new = pos1 - 0.5 * (r_new - r) * r_hat
    pos2_new = pos2 + 0.5 * (r_new - r) * r_hat

    # Moderate spin-up with cap
    v_mag = np.sqrt(G * (m1 + m2) / r_new) / 2
    tangential_dir = np.array([-r_hat[1], r_hat[0]])
    closeness = 1 - r_new / init_dist

    boost_factor = 3.0
    spin_multiplier = 1 + boost_factor * closeness**2
    spin_multiplier = min(spin_multiplier, 2.3775)  # Cap the multiplier

    v1_new = v_mag * tangential_dir * spin_multiplier
    v2_new = -v1_new

    return pos1_new, pos2_new, v1_new, v2_new
```

However, we posted this code to many sources on reddit, (most notably [here](https://www.reddit.com/r/astrophysics/comments/1m8u642/we_built_a_set_of_space_physics_simulations_in/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)) and received feedback pushing for a more realistic inspiral and merger.

The code above models mostly a 0 Post-Newtonian Order Approximation. If you want to read more into that, you can do so [here](https://en.wikipedia.org/wiki/Post-Newtonian_expansion). 

Therefore, we wanted to expand into the 1PN and 2.5PN range. However, these methods required a lot more computation and a little more thorough understanding of Newtonian Expansion. Before we could do all that, we had to switch our integrator to [Runge-Kutta 4](https://youtu.be/dShtlMl69kY?si=QEOEKR7CyPpI1mkj). With this knowledge, we created an integrator that returns positions and velocities with: 
```
def rk4_step(r1, r2, v1, v2, dt):
    """4th order Runge-Kutta integrator with post-Newtonian corrections."""
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
```
After this Runge-Kutta 4 Integrator, we needed to switch our acceleration methods to a 2.5PN order. However, 2.5 PN is very weak and simulates energy loss so we had to model 1PN first. Using the equations from [here](https://arxiv.org/abs/gr-qc/0010014?), we translated this into code. 
> [a1 = a_newton + a_1PN + a_2.5PN]. That logic will provide your acceleration of your forces.

The code to compute accelerations can be found below:
```
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
  ```

## Results

We simulated a binary pulsar with two neutron stars that also contained an inspiral and energy decay to cause a merger.

## Sources

[Post-Newtonian Equations]((https://arxiv.org/abs/gr-qc/0010014?))
[MatPlotLib FuncAnimation](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html)
[Post-Newtonian Expansion](https://en.wikipedia.org/wiki/Post-Newtonian_expansion)
[Runge-Kutta 4](https://youtu.be/dShtlMl69kY?si=QEOEKR7CyPpI1mkj)
[Peters Mathews Formula](https://ui.adsabs.harvard.edu/abs/1996NCimB.111..631P/abstract)
[Peters Mathews Equation](https://www.roma1.infn.it/teongrav/VESF/SCHOOL2013_WEBSITE/LECTURES/VESFnotes_Blanchet.pdf)
[Velocity Verlet](https://www.youtube.com/watch?v=1bwsy26x24Q)
[Kilonova](https://en.wikipedia.org/wiki/Kilonova)
[Binary Pulsars](https://en.wikipedia.org/wiki/Binary_pulsar)
