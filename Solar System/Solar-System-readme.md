# Solar-System Simulation
This simulation models the Solar System with Velocity Verlet and Gravitational Forces in Python.

## Problem

After we created the Sun-Earth-Moon system, expanding to a solar system was the next step.
We wanted to simualte Eight Planets in orbit around a Center of Mass (The Sun) with accurate
gravitational pulls and sizes.

## Approach

Simulation of a 9-body System with Euler Step was very unstable and didn't return accuracy.
Therefore, we switched to [Velocity Verlet](https://youtu.be/1bwsy26x24Q?si=KS2xWUzbPWM_i8P1).
After switching to Velocity Verlet, all planets must have forces from all OTHER planets along with the Sun
acting upon it. 

Therefore, switching to a class system with a loop to account for all planetary forces was imposed:
```
class Planet:
    def __init__(self, name, mass, pos, vel):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=float)
        self.velocity = np.array(vel, dtype=float)
        self.acceleration = np.zeros(2)
```

```
def velocity_verlet_step(planets, dt):
    for p in planets:
        p.pos += p.velocity * dt + 0.5 * p.acceleration * dt ** 2

    old_accelerations = [p.acceleration.copy() for p in planets]
    compute_acceleration(planets)

    for p, a_old in zip(planets, old_accelerations):
        p.velocity += 0.5 * (a_old + p.acceleration) * dt
```
After imposing planetary forces, (however small they may be) we had to plot with the `FuncAnimation` tool.

>Using Classes and For Loops saved us most of the time.

Additionally, we added a `zoom` toggle to set focus on Inner Planets, or All Planets: without Zoom, it was hard to see inner planetary orbits.
## Results

This project simulates all 8 planets orbiting the Sun using Newtonian gravity and basic numerical integration. It models the gravitational attraction between the Sun and the planets, allowing them to follow elliptical-like orbits with realistic parameters.

## Sources

>[Velocity Verlet Algorithm](https://www.youtube.com/watch?v=1bwsy26x24Q)
[MatPlotLib FuncAnimation](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html)
>[NASA Planet Data](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)
[Newton's Law of Universal Gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation)

