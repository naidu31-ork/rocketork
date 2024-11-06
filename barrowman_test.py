import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class nosecone_terms:
    def __init__(self, l_n=None):
        self.l_n = l_n

        self.X_n_cone = 0.666 * self.l_n
        self.X_n_ogive = 0.466 * self.l_n
        self.X_n_vonkarman = 0.5  * self.l_n
        self.X_n_lvhaack = 0.437 * self.l_n
        self.X_n_elliptical = 1.5 * self.l_n

    def calculate_C_nn(self):
        return 2

    def calculate_Xn_cone(self):
        return self.X_n_cone

    def calculate_Xn_ogive(self):
        return self.X_n_ogive
    
    def calculate_Xn_vonkarman(self):
        return self.X_n_vonkarman
    
    def calculate_Xn_lvhaack(self):
        return self.X_n_lvhaack
    
    def calculate_Xn_elliptical(self):
        return self.X_n_elliptical

    def describe(self):
        print(f"Length of nosecone: {self.l_n}")

class conical_transition_terms:
    def __init__(self, transition_len=None, d_f=None, d_r=None, d=None, X_P=None):
        self.transition_len = transition_len
        self.d_f = d_f
        self.d_r = d_r
        self.d = d
        self.X_P = X_P

    def calculate_C_nt(self):
        return 2 * ((self.d_r / self.d)**2 - (self.d_f / self.d)**2)

    def calculate_X_t(self):
        return self.X_P + (self.transition_len / 3) * (1 + (1 / (1 + (self.d_f / self.d_r))))

    def describe(self):
        print(f"Length of transition: {self.transition_len}")
        print(f"Diameter at front of transition: {self.d_f}")
        print(f"Diameter at rear of transition: {self.d_r}")
        print(f"Diameter at base of nosecone: {self.d}")
        print(f"Distance from nosecone tip to front of transition: {self.X_P}")

class fin_terms:
    def __init__(self, fin_count=None, aft_radius=None, fin_semispan=None, d=None, l_f=None, f_r=None, f_t=None, X_B=None, X_R=None):
        self.fin_count = fin_count
        self.aft_radius = aft_radius
        self.fin_semispan = fin_semispan
        self.d = d
        self.l_f = l_f
        self.f_r = f_r
        self.f_t = f_t
        self.X_B = X_B
        self.X_R = X_R

    def calculate_C_nf(self):
        return (1 + (self.aft_radius / (self.aft_radius + self.fin_semispan))) * ((4 * self.fin_count * ((self.fin_semispan / self.d)**2)) / (1 + ((1 + (((2 * self.l_f) / (self.f_r + self.f_t)))**2)**0.5)))

    def calculate_X_f(self):
        return self.X_B + (self.X_R / 3) * ((self.f_r + (2 * self.f_t)) / (self.f_r + self.f_t)) + (1 / 6) * ((self.f_r**2 + self.f_t**2 + (self.f_r*self.f_t)) / (self.f_r + self.f_t))

    def describe(self):
        print(f"Number of fins: {self.fin_count}")
        print(f"Rocket radius at aft end: {self.aft_radius}")
        print(f"Diameter at base of nosecone: {self.d}")
        print(f"Semi span of fin: {self.fin_semispan}")
        print(f"Mid-chord length of fin: {self.l_f}")
        print(f"Root chord of fin: {self.f_r}")
        print(f"Tip chord of fin: {self.f_t}")
        print(f"Distance between fin root leading edge and fin tip leading edge parallel to body: {self.X_R}")
        print(f"Distance from nose tip to fin root chord leading edge: {self.X_B}")
    
def calculate_Cp_location():
  return (((nosecone_terms.calculate_C_nn()*nosecone_terms.calculate_Xn_cone())+(conical_transition_terms.calculate_C_nt()*conical_transition_terms.calculate_X_t())+(fin_terms.calculate_C_nf()*fin_terms.calculate_X_f))/(fin_terms.calculate_C_nf() + conical_transition_terms.calculate_C_nt() + nosecone_terms.calculate_C_nn()))