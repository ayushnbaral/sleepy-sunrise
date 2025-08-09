jupiter_data = {
    "jupiter": [1.898e27, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
}

orbital_params = {# Orbital parameters for moons: [mass, orbital_radius, orbital_speed, inclination]
    # Galilean moons
    "io":        [8.93e22,   421.7e6,   17340.0, 0.036],
    "europa":    [4.80e22,   671.1e6,   13740.0, 0.47],
    "ganymede":  [1.48e23,   1.0704e9,  10880.0, 0.20],
    "callisto":  [1.08e23,   1.8827e9,  8200.0,  0.28],

    # Inner moons
    "metis":      [9.56e16,   127.97e3,   31570.0, 0.06],
    "adrastea":   [1.91e17,   128.98e3,   31490.0, 0.05],
    "amalthea":   [2.08e18,   181.4e3,    26080.0, 0.37],
    "thebe":      [7.77e17,   221.9e3,    23440.0, 1.08],

    # Prograde irregulars (Himalia group and others)
    "themisto":   [6.9e15,    7.5e6,      8300.0,  43.1],
    "leda":       [1.0e16,    11.16e6,    7350.0,  27.5],
    "ersa":       [8.0e15,    11.7e6,     7200.0,  30.5],
    "pandia":     [9.0e15,    11.7e6,     7200.0,  29.2],
    "dia":        [9.0e15,    12.6e6,     7050.0,  28.2],
    "carpo":      [1.0e16,    17.1e6,     6300.0,  51.4],
    "valetudo":   [1.0e16,    18.0e6,     6100.0,  34.0],
    "himalia":    [4.2e18,    11.46e6,    7250.0,  27.5],
    "elara":      [8.7e17,    11.7e6,     7250.0,  26.6],
    "lysithea":   [7.5e17,    11.1e6,     7350.0,  26.3],
    "eupheme":    [1.0e16,    19.2e6,     5950.0,  145.0],  # Note: usually retrograde, incl. for completeness
    "orthosie":   [1.0e16,    20.2e6,     5800.0,  146.0],
    "thyone":     [1.0e16,    20.5e6,     5750.0,  146.5],
    "hermippe":   [1.0e16,    20.7e6,     5700.0,  147.0],
    "iocaste":    [1.0e16,    20.9e6,     5650.0,  148.0],

    # Retrograde irregulars (Pasiphae, Carme, Ananke groups)
    "euporie":    [1.0e16,    19.3e6,     5950.0,  145.8],
    "sponde":     [1.0e16,    24.0e6,     5450.0,  157.2],
    "autonoe":    [1.0e16,    24.3e6,     5400.0,  152.8],
    "callirrhoe": [1.0e16,    24.1e6,     5420.0,  141.8],
    "megaclite":  [1.0e16,    24.7e6,     5380.0,  150.0],
    "taygete":    [1.0e16,    23.4e6,     5480.0,  165.0],
    "chaldene":   [1.0e16,    23.0e6,     5500.0,  166.0],
    "harpalyke":  [1.0e16,    21.1e6,     5650.0,  148.6],
    "pasiphae":   [3.0e17,    23.5e6,     5470.0,  151.4],
    "sinope":     [7.5e16,    23.8e6,     5450.0,  158.0],
    "kalyke":     [7.5e16,    23.1e6,     5500.0,  165.0],
    "eukelade":   [7.5e16,    23.5e6,     5450.0,  164.0],
    "philophrosyne":[7.5e16,  23.7e6,     5430.0,  157.0],
    "ananke":     [1.0e17,    21.3e6,     5600.0,  148.9],
    "carme":      [1.0e17,    23.4e6,     5480.0,  165.0],
}

moon_colors = {
    # Jupiter itself
    "jupiter": "orange",

    # Galilean moons (each unique, bright)
    "io": "gold",
    "europa": "deepskyblue",
    "ganymede": "peru",
    "callisto": "orchid",

    # Inner moons (bright whites/grays)
    "metis": "white",
    "adrastea": "white",
    "amalthea": "gainsboro",  # slightly gray so not blinding
    "thebe": "silver",

    # Prograde irregulars (bright greens)
    "themisto": "limegreen",
    "leda": "springgreen",
    "ersa": "limegreen",
    "pandia": "mediumspringgreen",
    "dia": "chartreuse",
    "carpo": "lime",
    "valetudo": "palegreen",
    "himalia": "forestgreen",
    "elara": "mediumseagreen",
    "lysithea": "yellowgreen",

    # Retrograde irregulars (deep reds)
    "eupheme": "darkred",
    "orthosie": "indianred",
    "thyone": "brown",
    "iocaste": "red",
    "hermippe": "firebrick",
    "euporie": "crimson",
    "sponde": "firebrick",
    "autonoe": "darkred",
    "callirrhoe": "indianred",
    "megaclite": "maroon",
    "taygete": "brown",
    "chaldene": "darkred",
    "harpalyke": "firebrick",
    "pasiphae": "red",
    "sinope": "darkred",
    "kalyke": "brown",
    "eukelade": "firebrick",
    "philophrosyne": "indianred",
    "ananke": "maroon",
    "carme": "darkred",
}


moon_alpha = moon_colors.copy()
for key in moon_colors:
    '''initializing transparency for viewing certain groups'''
    moon_alpha[key] = 1

moon_sizes = {
    "jupiter": 16,
    "io": 3,
    "europa": 3,
    "ganymede": 4,
    "callisto": 4,

    # Inner moons a bit smaller
    "metis": 1.5,
    "adrastea": 1.5,
    "amalthea": 2,
    "thebe": 2,

    # Prograde irregulars small
    "themisto": 1,
    "leda": 1,
    "ersa": 1,
    "pandia": 1,
    "dia": 1,
    "carpo": 1,
    "valetudo": 1,
    "himalia": 2,
    "elara": 1.8,
    "lysithea": 1.8,
    "eupheme": 1,
    "orthosie": 1,
    "thyone": 1,
    "hermippe": 1,
    "iocaste": 1,

    # Retrograde irregulars small as well
    "euporie": 1,
    "sponde": 1,
    "autonoe": 1,
    "callirrhoe": 1,
    "megaclite": 1,
    "taygete": 1,
    "chaldene": 1,
    "harpalyke": 1,
    "pasiphae": 2,
    "sinope": 1.8,
    "kalyke": 1.8,
    "eukelade": 1,
    "philophrosyne": 1,
    "ananke": 1.5,
    "carme": 2,
}
