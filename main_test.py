from rocket_test import Rocket
from barrowman_test import nosecone_terms, conical_transition_terms, fin_terms
from aerodynamic_char_test import nosecone_drag, bodytube_drag, fin_drag, total_drag
import numpy as np

abhyuday = Rocket(
    upper_body_diameter=160/1000,
    lower_body_diameter = 115/1000,
    transition_length = 5/100,
    nose_diameter=160/1000,
    upper_body_length=0.56,
    lower_body_length=1.54,
    mass= 18.119,
    inertia=(12.99, 12.99, 0.074),
    power_off_drag = "C:/Users/Balaji Naidu/Downloads/drag_off.csv",
    power_on_drag = "C:/Users/Balaji Naidu/Downloads/drag_on.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

rail_buttons = abhyuday.set_rail_buttons(
    upper_button_position=-0.2,
    lower_button_position=-0.873,
    angular_position=45,
)

nose_cone = abhyuday.add_nose(length=0.64, kind="elliptical", position=1.81)
fin_set = abhyuday.add_trapezoidal_fins(
    n=4,
    root_chord=0.305,
    tip_chord=0.15,
    span=0.2275,
    position=-0.01,
    cant_angle=np.deg2rad(0),
)

#abhyuday.plot_rocket()

nose_cone = nosecone_terms(l_n=0.64)
transition = conical_transition_terms(transition_len=0.05, d_f=0.16, d_r=0.115, d=0.16, X_P=1.2)
fins = fin_terms(fin_count=4, aft_radius=0.0575, fin_semispan=0.17, d=0.16, l_f=0.187, f_r=0.305, f_t=0.15, X_B=2.45, X_R=0.155)

C_nn = nose_cone.calculate_C_nn()
print(f"C_nn: {C_nn:.2f}")

X_n_vonkarman = nose_cone.calculate_Xn_vonkarman()
print(f"X_n_nose: {X_n_vonkarman:.4f}")

C_nt = transition.calculate_C_nt()
print(f"C_nt: {C_nt:.4f}")
X_t = transition.calculate_X_t()
print(f"X_t: {X_t:.4f}")

C_nf = fins.calculate_C_nf()
print(f"C_nf: {C_nf:.4f}")
X_f = fins.calculate_X_f()
print(f"X_f: {X_f:.4f}")

Cp_location = ((C_nn * X_n_vonkarman) + (C_nt * X_t) + (C_nf * X_f)) / (C_nn + C_nt + C_nf)
print(f"Center of Pressure Location: {Cp_location:.2f} meters")

speeds = np.linspace(50, 300, 10)  # Example speeds (m/s) during flight


machs = speeds/343 #provide provision for measurement of speed with temperature
# Calculate drag at each speed
for mach in machs:
    # Calculate drag due to the nosecone, bodytube, and fins at the given speed
    nose_drag = nosecone_drag(abhyuday, 0.5, mach)
    body_drag = bodytube_drag(abhyuday, mach)
    fin_drag_value = fin_drag(abhyuday, mach)
    
    # Calculate total drag
    total_drag_value = total_drag(nose_drag, body_drag, fin_drag_value)

    print(f"At speed {mach:.2f} m/s, Total Drag: {total_drag_value:.2f} N")