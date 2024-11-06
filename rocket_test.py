import matplotlib.pyplot as plt
import numpy as np

class Rocket:
    def __init__(self, upper_body_length, lower_body_length, transition_length, upper_body_diameter, lower_body_diameter, nose_diameter, mass, inertia, power_off_drag, power_on_drag, center_of_mass_without_motor, coordinate_system_orientation):
        self.upper_body_diameter = upper_body_diameter
        self.nose_diameter = nose_diameter
        self.upper_body_length = upper_body_length
        self.lower_body_length = lower_body_length
        self.lower_body_diameter = lower_body_diameter
        self.transition_length = transition_length
        self.mass = mass
        self.inertia = inertia
        self.power_off_drag = power_off_drag
        self.power_on_drag = power_on_drag
        self.center_of_mass_without_motor = center_of_mass_without_motor
        self.coordinate_system_orientation = coordinate_system_orientation
        self.nose_cone = None
        self.fins = []

    def set_rail_buttons(self, upper_button_position, lower_button_position, angular_position):
        self.upper_button_position = upper_button_position
        self.lower_button_position = lower_button_position
        self.angular_position = angular_position

    def add_nose(self, length, kind, position):
        self.nose_cone = {'length': length, 'kind': kind, 'position': position}

    def add_trapezoidal_fins(self, n, root_chord, tip_chord, span, position, cant_angle):
        self.fins.append({'n': n, 'root_chord': root_chord, 'tip_chord': tip_chord, 'span': span, 'position': position, 'cant_angle': cant_angle})


    def plot_rocket(self):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot body tube
        body_radius = self.upper_body_diameter / 2

        upper_body_radius = self.upper_body_diameter / 2
        lower_body_radius = self.lower_body_diameter /2
        nose_length = self.nose_cone['length']
        nose_position = self.nose_cone['position']
        rear_diameter = self.nose_diameter

        if self.nose_cone and self.nose_cone['kind'] == 'vonkarman':

            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            theta_ = np.arccos(1 - ((2 * (x_curve - nose_position)) / nose_length))
            y_curve = (rear_diameter / (2 * np.sqrt(np.pi))) * np.sqrt(theta_ - (np.sin(2 * theta_) / 2))

            ax.plot(-(x_curve - nose_position)+nose_position+nose_length, y_curve, color='black')
            ax.plot(-(x_curve - nose_position)+nose_position+nose_length, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'] == 'conical':

            ax.plot([nose_position + nose_length, nose_position], [0, rear_diameter/2], color='black')
            ax.plot([nose_position + nose_length, nose_position], [0, -rear_diameter/2], color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'] == 'elliptical':

            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            theta_ = x_curve/nose_length
            y_curve = (rear_diameter/2) * np.sqrt(1 - ((x_curve - nose_position)/nose_length)**2)

            ax.plot(x_curve, y_curve, color='black')
            ax.plot(x_curve, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'] == 'tangent_ogive':

            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            x_curve_2 = np.linspace(nose_length, 0, num_points)
            rho_ = ((rear_diameter/2)**2 + (nose_length)**2)/(rear_diameter)
            y_curve = np.sqrt(rho_**2 - ((nose_length - x_curve_2)**2)) + (rear_diameter/2) - rho_

            ax.plot(x_curve, y_curve, color='black')
            ax.plot(x_curve, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'].startswith('power_series'):
            power_value = float(self.nose_cone['kind'].split('_')[-1])
            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            x_curve_2 = np.linspace(nose_length, 0, num_points)
            y_curve = (rear_diameter/2)*(x_curve_2/nose_length)**(power_value)

            ax.plot(x_curve, y_curve, color='black')
            ax.plot(x_curve, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'].startswith('parabolic'):
            power_value = float(self.nose_cone['kind'].split('_')[-1])
            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            x_curve_2 = np.linspace(nose_length, 0, num_points)
            y_curve = (rear_diameter/2)*((2*(x_curve_2/nose_length) - power_value*((x_curve_2/nose_length)**2))/(2- power_value))**(power_value)

            ax.plot(x_curve, y_curve, color='black')
            ax.plot(x_curve, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')

        if self.nose_cone and self.nose_cone['kind'].startswith('haack'):
            power_value = float(self.nose_cone['kind'].split('_')[-1])
            num_points = 100
            x_curve = np.linspace(nose_position, nose_position + nose_length, num_points)
            x_curve_2 = np.linspace(nose_length, 0, num_points)
            theta_ = np.arccos(1 - ((2 * (x_curve_2)) / nose_length))
            y_curve = (rear_diameter / (2 * np.sqrt(np.pi))) * np.sqrt(theta_ - (np.sin(2 * theta_) / 2) + (power_value*(np.sin(theta_)**3)))

            ax.plot(x_curve, y_curve, color='black')
            ax.plot(x_curve, -y_curve, color='black')
            ax.plot([nose_position, nose_position], [upper_body_radius, -upper_body_radius], color='black')


        ax.plot([nose_position , nose_position  - self.upper_body_length], [upper_body_radius, upper_body_radius], color='black')
        ax.plot([nose_position , nose_position  - self.upper_body_length], [-upper_body_radius, -upper_body_radius], color='black')
        ax.plot([nose_position - self.upper_body_length , nose_position  - self.upper_body_length], [upper_body_radius, -upper_body_radius], color='black')

        ax.plot([nose_position  - self.upper_body_length, nose_position - self.upper_body_length - self.transition_length], [upper_body_radius, lower_body_radius], color='green')
        ax.plot([nose_position  - self.upper_body_length, nose_position - self.upper_body_length - self.transition_length], [-upper_body_radius, -lower_body_radius], color='green')
        ax.plot([nose_position - self.upper_body_length - self.transition_length, nose_position  - self.upper_body_length - self.transition_length], [lower_body_radius, -lower_body_radius], color='green')

        ax.plot([nose_position  - self.upper_body_length - self.transition_length , nose_position  - self.upper_body_length - self.lower_body_length - self.transition_length], [lower_body_radius, lower_body_radius], color='black')
        ax.plot([nose_position  - self.upper_body_length - self.transition_length , nose_position  - self.upper_body_length - self.lower_body_length - self.transition_length], [-lower_body_radius, -lower_body_radius], color='black')
        ax.plot([nose_position - self.upper_body_length - self.lower_body_length - self.transition_length, nose_position  - self.upper_body_length - self.lower_body_length - self.transition_length], [lower_body_radius, -lower_body_radius], color='black')


        for fin in self.fins:
            root_chord = fin['root_chord']
            tip_chord = fin['tip_chord']
            span = fin['span']
            position = fin['position']
            cant_angle = fin['cant_angle']
            half_span = span / 2
            ax.plot([position, position - root_chord + tip_chord, position - root_chord, position - root_chord, position], [lower_body_radius, lower_body_radius + half_span, lower_body_radius + half_span, lower_body_radius, lower_body_radius], color='black')

            x = [position, position - root_chord + tip_chord, position - root_chord, position - root_chord, position]
            y = [lower_body_radius, lower_body_radius + half_span, lower_body_radius + half_span, lower_body_radius, lower_body_radius]
            ax.fill(x, y, color='red')

            ax.plot([position, position - root_chord + tip_chord, position - root_chord, position - root_chord, position], [-lower_body_radius, -lower_body_radius - half_span, -lower_body_radius - half_span, -lower_body_radius, -lower_body_radius], color='black')


            a = [position, position - root_chord + tip_chord, position - root_chord, position - root_chord, position]
            b = [-lower_body_radius, -lower_body_radius - half_span, -lower_body_radius - half_span, -lower_body_radius, -lower_body_radius]
            ax.fill(a, b, color='red')

        ax.set_xlim(-0.7, max([self.nose_cone['position'], max([fin['position'] for fin in self.fins])])+1)
        ax.set_ylim(-max(self.upper_body_diameter, self.nose_diameter)/2-0.2, max(self.upper_body_diameter, self.nose_diameter)/2+0.2)
        ax.set_aspect('equal')

        plt.title(" Rocket's Side View")

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.show()