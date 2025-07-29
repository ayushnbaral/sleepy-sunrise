[![Sleepy Sunrise](https://img.shields.io/badge/YouTube-Sleepy__Sunrise-red?logo=youtube&style=for-the-badge)](https://www.youtube.com/@sleepy-sunrise)

# ☀️ Sleepy Sunrise — A Physics Modeling Project

**Developed by Archith Sridhar and Ayush Baral**

We are rising high school juniors with a strong interest in physics and applied mathematics.  
This project is a collaborative effort to explore and visualize fundamental physical systems through computational modeling.
## ✅ Requirements

### 💻 Python Version
- Python **3.7 or higher** (recommended: 3.8+)

### 📦 Python Libraries
The simulations require these packages:

- `numpy` — for numerical computations  
- `matplotlib` — for plotting and animations

Install them using:

```bash
pip install numpy matplotlib
```
---

## Completed Projects

Our current modules focus on **gravitational modeling and orbital dynamics**, including:

### 🔭 `kilonova/`
A dynamic simulation of two neutron stars in a decaying binary orbit, spiraling inward due to gravitational wave radiation and eventually merging in a kilonova explosion.  
- **Physics Modeled:** Gravitational wave-driven orbital decay (Peters-Mathews approximation), realistic mass and radius of neutron stars, and relativistic effects on separation.  
- **Visual Features:** Trails showing orbital paths, a smooth merger explosion with expanding ejecta particles, and color transitions representing heat dissipation.  
- **Integration Method:** Velocity Verlet integration for numerical stability during tight orbital motion.

---

### ☀️ `solar_system/`
Models the entire solar system with the Sun and 8 planets orbiting under Newtonian gravity.  
- **Physics Modeled:** Central force motion governed by Newton’s Law of Gravitation, scaled planetary distances and masses.  
- **Visual Features:** Adjustable zoom mode to visualize outer planets, smooth orbital trajectories, and accurate elliptical motion.  
- **Integration Method:** Uses Verlet to maintain stability for long-term orbital behavior.

---

### 🌙 `earth_moon/`
Simulates the Earth-Moon system in two-body motion, emphasizing circular orbital dynamics and gravitational attraction.  
- **Physics Modeled:** Gravitational force between Earth and Moon, using real-world mass and distance values.  
- **Visual Features:** Simple and clean visualization of a stable orbit, with options to visualize angular velocity or energy.  
- **Integration Method:** Explicit Euler step — easy to implement but less accurate for long-term stability.

---

### 🌌 `three_body/`
Demonstrates the complex and chaotic behavior of a three-body gravitational system, such as the Sun–Earth–Moon configuration.  
- **Physics Modeled:** Mutual gravitational attraction between all three masses, leading to nonlinear, unpredictable trajectories.  
- **Visual Features:** Orbital trails that often diverge, allowing users to observe how small changes in position or velocity affect long-term motion.  
- **Use Case:** Ideal for visualizing chaotic systems and understanding why exact prediction becomes impossible in three-body problems.

---

## 🧠 Skills Demonstrated

| Simulation      | Physics Topics                  | Programming Skills                  | Numerical Methods           |
|----------------|----------------------------------|-------------------------------------|-----------------------------|
| `kilonova/`     | Gravitational waves, binary orbits | Numpy, animation, particle systems  | Velocity Verlet Integration |
| `solar_system/` | Newtonian gravity, planetary motion | Scaling, zoom, multi-body systems   | Velocity Verlet Integration  |
| `earth_moon/`   | Two-body motion, real-world modeling | Simple simulation design            | Euler Method                |
| `three_body/`   | Chaos, nonlinear interactions     | Generalized force loops, plotting   | Euler Integration  |

- **Languages & Libraries:** Python, NumPy, Matplotlib, FuncAnimation  
- **Physics Topics:** Newtonian gravity, orbital mechanics, circular motion, numerical integration (Velocity Verlet)

---

## 🚀 Project Goals

This repository serves as a learning sandbox for deepening our understanding of classical mechanics and computational physics.

### Future Plans:
- N-body gravitational systems  
- Multi-moon or binary star simulations  
- Electromagnetic field and collision visualizations  
- Drag Modeling

---

## 📌 Purpose

Our goal is to document our progress and create accessible visual simulations that reflect both our learning and curiosity.  
This is an ongoing collaborative project that we will continue to expand as our skills and interests grow.
