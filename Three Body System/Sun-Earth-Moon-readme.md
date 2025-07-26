# Sun-Earth-Moon System
This simulation models the Sun-Earth-Moon system with Velocity Verlet and Gravitational Forces in Python.

## Problem

We wanted to approach a real-life example of a three-body problem before we got into n-body simulations. Therefore, we started with the Sun-Earth-Moon. However, to prepare ourselves for n-body simulations, we made sure that the forces were accurate with Gravitational and Newtonian Physics.

## Approach

To make it realistic, we had to first initialize our data. Using [NASA Planet Data](https://nssdc.gsfc.nasa.gov/planetary/factsheet/) we set up realistic conditions. Then, we employed the [Euler Step](https://en.wikipedia.org/wiki/Euler_method) to enforce gravitational forces on all three bodies from one other. Because there wasn't too many bodies and our system was very controlled, Euler Step seemed good enough. 
```
    # Forces
    r_es = pos_earth - pos_sun
    f_earth = -G * M_sun * M_earth / np.linalg.norm(r_es)**3 * r_es

    r_me = pos_moon - pos_earth
    f_moon_from_earth = -G * M_earth * M_moon / np.linalg.norm(r_me)**3 * r_me

    r_ms = pos_moon - pos_sun
    f_moon_from_sun = -G * M_sun * M_moon / np.linalg.norm(r_ms)**3 * r_ms

    # Accelerations
    a_earth = f_earth / M_earth
    a_moon = (f_moon_from_earth + f_moon_from_sun) / M_moon

    # Euler update
    vel_earth += a_earth * dt
    vel_moon += a_moon * dt
    pos_earth += vel_earth * dt
    pos_moon += vel_moon * dt
```
This was good enough and gave a somewhat accurate representation of the Sun-Earth-Moon system. However, we wanted more accuracy, which led us to find the Verlet Integration method for our future projects. 

## Results

We simulated a real-world Three Body System: Sun-Earth-Moon. The scale of the system was so large that it was hard to see the moon orbiting Earth, which led us to add the `zoom` toggle to see the Moon-Earth System as well.

## Sources

>[Euler Step](https://en.wikipedia.org/wiki/Euler_method)
[MatPlotLib FuncAnimation](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html)
>[NASA Planet Data](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)
[Newton's Law of Universal Gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation)
