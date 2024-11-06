import numpy as np
from abhyuday_ork_solver import Rocket, predict_apogee

def test_apogee_prediction():
    
    #Altitude at motor burnout
    altitude = 893.4
    velocity_vector = np.array([11.85, 0, 275])  

    angle_x = np.radians(0)  #Pitch
    angle_y = np.radians(2.46)  #Yaw
    angle_z = np.radians(0)  #Roll

    orientation_matrix = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    #This can be declared in the main file with FC code
    rocket = Rocket(
        nosecone_diameter = 0.16, 
        nosecone_length = 0.72, 
        body_tube_length = 3.24, 
        body_tube_diameter = 0.16,
        boat_tail_length = 0.08, 
        boat_tail_fore_diameter = 0.16, 
        boat_tail_aft_diameter = 0.01, 
        fin_height = 0.15, 
        fin_span = 0.46, 
        rocket_weight = 33.75, 
        A_wet_body = 1.82, 
        A_wet_fin = 0.0840,
        fin_t = 0.003, 
        fin_mac = 0.530,
    )

    #Keep calling this file by suplying it with diff altitudes (extracted from the barometric sensor) 
    #And orientation data (extracted from the IMU)
    apogee = predict_apogee(altitude, velocity_vector, orientation_matrix, rocket)
    
    print(f"Apogee: {apogee:.2f} m.")

if __name__ == "__main__":
    test_apogee_prediction()