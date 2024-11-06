# drag_calculations.py
import numpy as np
from rocket_test import Rocket

def nosecone_drag(Rocket, nose_cone_length, speed):
    # Drag due to nosecone (speed-dependent)
    return 4 * nose_cone_length * (Rocket.nose_diameter ** 2) * (speed ** 2)

def bodytube_drag(Rocket, speed):
    # Drag due to bodytube (speed-dependent)
    return (1 / speed) * Rocket.lower_body_length * (Rocket.upper_body_diameter ** 2)

def fin_drag(Rocket, speed):
    # Drag due to fins (speed-dependent)
    return 0.5 * 0.5* 0.01 * (speed ** 2)

def total_drag(nose_drag, body_drag, fin_drag):
    # Total drag is the sum of all component drags
    return nose_drag + body_drag + fin_drag