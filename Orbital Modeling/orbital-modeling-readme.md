# 🌙 Earth–Moon Orbit Simulation

This simulation models the Moon orbiting a stationary Earth using trigonometric functions, introducing us to orbital mechanics in a simplified environment.

# How to Run:
```
cd earth_moon
python earth_moon.py
```

## Problem

For our very first physics project, neither of us had extensive Gravitational or Relativistic Knowledge, 
so we decided to go *small-scale* and simulate one object orbiting another stationary object with a pre-planned orbit.

Initially, we planned to have a satellite orbit the Earth; however, we then expanded into a Earth-Moon System
so we could possibly expand or build on top of that in the future.

## Approach

Having the Earth in the center, we could pre-plan the orbit of the moon and allow it to travel along that orbit.
Using cosine and sine functions, we arrived at a circular orbit with no eccentricity:
```
orbit_x = moon_distance * np.cos(orbit_theta)
orbit_y = moon_distance * np.sin(orbit_theta)
```
These are [Polar Coordinates](https://en.wikipedia.org/wiki/Polar_coordinate_system) that model the circular orbit.

After this, we wanted to animate the orbit of the Moon around the Earth. 

Using certain libraries like: ```matplotlib, FuncAnimation```, we could animate and plot the orbit of the system.
After intitializing positions and creating an update function that "updates" positions by frame, we had to call
```
ani = FuncAnimation(
    fig, update, frames=frames,
    init_func=init, interval=interval, blit=True
)
```
This resulted in an orbit of the moon around the Earth, through polar coordinates. There was no Gravitational Elements or
Integration Functions at this point of time.

## Results

We created an orbit of the moon around the earth that modeled a real-world system. It was vital in getting our foot in the door,
and exposing us to physics concepts. Though it could've been more realistic, we learned about the process itself behind the scenes.

