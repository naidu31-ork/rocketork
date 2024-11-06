import numpy as np

g = 9.81
rho_air = 1.23
dt = 0.01
mu_air = 0.0000185

class Rocket:
    def __init__(self, nosecone_diameter, nosecone_length, body_tube_length, body_tube_diameter, boat_tail_length, boat_tail_fore_diameter, boat_tail_aft_diameter, fin_height, fin_span, rocket_weight, A_wet_body, A_wet_fin, fin_t, fin_mac):
        
        self.nosecone_diameter = nosecone_diameter
        self.nosecone_length = nosecone_length
        self.body_tube_length = body_tube_length
        self.body_tube_diameter = body_tube_diameter
        self.boat_tail_length = boat_tail_length
        self.boat_tail_fore_diameter = boat_tail_fore_diameter
        self.boat_tail_aft_diameter = boat_tail_aft_diameter
        self.fin_height = fin_height
        self.fin_span = fin_span
        self.rocket_weight = rocket_weight
        self.A_wet_body = A_wet_body
        self.A_wet_fin = A_wet_fin
        self.fin_t = fin_t
        self.fin_mac = fin_mac


def reynolds_number(velocity, characteristic_length):
    Re = (rho_air * velocity * characteristic_length) / mu_air
    return Re

def drag_force(velocity_vector, rocket):
    
    speed = np.linalg.norm(velocity_vector)  
    mach = (speed/340)
    fineness_r = (rocket.body_tube_length + rocket.nosecone_length)/rocket.body_tube_diameter
    A_ref = 0.0201
    
    def drag_skin_friction():
        if reynolds_number(speed, 0.16) < 10000:
            Cf_skin_friction_est = 0.0148
        if 10000 < reynolds_number(speed, 0.16) < 51*((0.00006/0.16))**(-1.039):
            Cf_skin_friction_est = 1/(((1.5*np.log(reynolds_number(speed, 0.16))) - 5.6)**2) 
        else:
            Cf_skin_friction_est = 0.032*((0.00006/0.16)**(0.2))
        Cf_skin_friction = Cf_skin_friction_est*(1- (0.1*(mach**2)))
        Cd_skin_friction = (Cf_skin_friction/A_ref)*((1 + (0.5/fineness_r))*rocket.A_wet_body + (1 + (2*rocket.fin_t/rocket.fin_mac))*rocket.A_wet_fin)
        print(Cd_skin_friction)
        
        return   0.5 * Cd_skin_friction * rho_air * A_ref * (speed**2)
    
    def drag_nosecone():
        Cd_nosecone = 0.1  
        A_nosecone = np.pi * (rocket.nosecone_diameter / 2) ** 2 
        return 0 

    def drag_body_tube():
        Cd_body_tube = 0.5  
        A_body_tube = rocket.body_tube_length * rocket.body_tube_diameter  
        return 0 

    def drag_fins():
        Cd_fins = ((1 - mach**2))**(-0.417) - 1 + (0.12 + 0.13*((mach)**2))
        A_fins = 4 * rocket.fin_height * rocket.fin_t  
        A_canards = 4 * 0.075 * 0.003
        return 0.5 * Cd_fins * (A_fins) * rho_air * (speed ** 2) 

    def drag_boat_tail():
        gamma = (rocket.boat_tail_length)/(rocket.boat_tail_fore_diameter - rocket.boat_tail_aft_diameter)
        A_boat_tail = np.pi * 0.25 * (rocket.boat_tail_fore_diameter + rocket.body_tube_diameter) * ((((rocket.boat_tail_fore_diameter - rocket.boat_tail_aft_diameter)**2)*0.25 + rocket.boat_tail_length**2)**0.5)  # Boat tail surface area
        if gamma < 1 :
            Cd_boat_tail = (A_ref/A_boat_tail)*(0.12 + 0.13*((mach)**2)) + (0.12 + 0.13*((mach)**2))
        if 1 < gamma < 3 :
            Cd_boat_tail = (A_ref/A_boat_tail)*(0.12 + 0.13*((mach)**2))*(3-gamma)/2 + (0.12 + 0.13*((mach)**2))
        if gamma > 3 :
            Cd_boat_tail = (0.12 + 0.13*((mach)**2))
        
        return 0.5 * Cd_boat_tail * np.pi * (rocket.boat_tail_aft_diameter)**2 * 0.25 * rho_air * speed**2

    

    #print('skin friction')
    #drag_skin_friction()
    #print('\n')
    #print('Speed')
    #print(np.linalg.norm(velocity_vector))
    total_drag_magnitude =   drag_boat_tail()  + drag_fins()  + drag_skin_friction()
    #print(total_drag_magnitude)
    drag_vector = -total_drag_magnitude * velocity_vector / speed
    #print('\n')
    #print(velocity_vector)

    return drag_vector


def update_state(altitude, velocity_vector, orientation_matrix, rocket):
    
    gravity_vector = [0, 0, -9.81]
    drag_vector = drag_force(velocity_vector, rocket)
    total_acceleration = (drag_vector / rocket.rocket_weight) + gravity_vector  
    velocity_new = velocity_vector + total_acceleration * dt
    altitude_new = altitude + velocity_vector[2] * dt
    #print(altitude_new)

    return altitude_new, velocity_new

def predict_apogee(altitude, velocity_vector, orientation_matrix, rocket):
    
    while velocity_vector[2] > 0: 
        altitude, velocity_vector = update_state(altitude, velocity_vector, orientation_matrix, rocket)

    return altitude