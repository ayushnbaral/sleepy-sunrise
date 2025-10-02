# Multi-Moon
This simulation models Four Groups of Jupiter's Moons.
Here's a list of [Jupiter's Moons](https://science.nasa.gov/jupiter/jupiter-moons/all-jupiter-moons/), however do note that we modeled the Inner Moon Group, Retrograde Moon Group, Prograde Moon Group, and the Galilean Moon Group.
## Problem

We wanted to model a Jupiter's Moons using MatPlotLib and Python. However, we decided to model it in an interactive 3D simulation using its [FuncAnimation](https://matplotlib.org/stable/users/explain/animations/animations.html) tool.

## Approach

We had already built a solar system before, however that was in a 2 Dimensional Space. To model a 3 Dimensional Simulation, we had to change our axes to 3D. [This](https://matplotlib.org/stable/api/toolkits/mplot3d.html#module-mpl_toolkits.mplot3d) is a good website to check out.

After scaling our axes to 3D, we then had to create a dictionary of all the Moons that we were going to model. Higher order Groups are most definitely possible to include, however for the sake of quality, we decided to include only the four most inner groups. For this, we made a separate file that was imported that contained all the moon data.

However, though all the moon data was visible, the time step was either too high for the inner moons or too low for the outer moons. Since RK4 is not symplectic and does not allow for dynamic timesteps, we reverted to Velocity Verlet. 

Through timestep manipulation by group:
```
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
```
we were able to view all four groups at the same time, without one flying off too early.

Additionally, Jupiter's shape is not spherical but more of an ellipse. Therefore, the graviational pull is different at different points of an orbit.
Through this line:
```
factor = - (3 * G * jupiter.mass * J2 * R_jup ** 2) / (2 * dist ** 5)
```
and defining [J2](https://ai-solutions.com/_freeflyeruniversityguide/j2_perturbation.htm) as 0.014736, we could artificially model this J2 Pertrubration.

Besides 3D Modeling, Dynamic Timestep, and J2 Petrubration, most of the code is virtually similar to the Solar System Code, since they both are n-body systems.

## Results

We simulated Jupiter's Moons in a Three Dimensional Space with Python.

## Sources
[J2](https://ai-solutions.com/_freeflyeruniversityguide/j2_perturbation.htm)
[3D MatPlotLib](https://matplotlib.org/stable/api/toolkits/mplot3d.html#module-mpl_toolkits.mplot3d)
[FuncAnimation](https://matplotlib.org/stable/users/explain/animations/animations.html)
[Jupiter's Moons](https://science.nasa.gov/jupiter/jupiter-moons/all-jupiter-moons/)
