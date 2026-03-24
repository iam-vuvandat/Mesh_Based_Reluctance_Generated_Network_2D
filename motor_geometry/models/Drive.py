import numpy as np 
import math 
import matplotlib.pyplot as plt

pi = math.pi

class Drive:
    def __init__(self, motor):
        self.motor = motor
        
        self.rotor_angle_offset =   pi / self.motor.pole_number 
        self.phase_number = self.motor.phase_number
        self.i_rms = self.motor.i_rms
        self._sync_dq_components()

    def _sync_dq_components(self):
        i_peak = self.i_rms * math.sqrt(2)
        self.id = 0.0
        self.iq = i_peak

    def get_drive_position(self):
        # Truy xuat vi tri goc tu reluctance_network
        rotor_position = self.motor.reluctance_network.rotor_position
        current_position = rotor_position + (self.rotor_angle_offset) * 1
        
        # In ra 2 bien de kiem tra debug
        print(f"rotor_position: {rotor_position:.4f} rad ({np.degrees(rotor_position):.2f} deg) | "
              f"current_position: {current_position:.4f} rad ({np.degrees(current_position):.2f} deg)")
              
        return current_position

    def get_theta_e(self):
        current_mechanical_position = self.get_drive_position()
        return current_mechanical_position * (self.motor.pole_number / 2)

    def calculate_n_phase_currents(self):
        theta_e = self.get_theta_e()
        
        i_alpha = self.id * math.cos(theta_e) - self.iq * math.sin(theta_e)
        i_beta  = self.id * math.sin(theta_e) + self.iq * math.cos(theta_e)
        
        current_phases = []
        for k in range(int(self.phase_number)):
            angle_shift = (2 * pi * k) / self.phase_number
            i_k = i_alpha * math.cos(angle_shift) + i_beta * math.sin(angle_shift)
            current_phases.append(i_k)
        return np.array(current_phases)

    def apply_winding_excitation(self, excitation = True):
        self.i_rms = self.motor.i_rms
        self._sync_dq_components()
        
        currents = self.calculate_n_phase_currents()
        if excitation is False:
            currents *= 0.0

        self.motor.reluctance_network.stator_excitation = currents

# ==========================================
# PHAN TEST CHO DONG CO 15 SLOT - 10 POLE
# ==========================================
if __name__ == "__main__":
    class MockReluctanceNetwork:
        def __init__(self):
            self.rotor_position = 0.0
        def update_reluctance_network(self, winding_current, update_for_winding_current):
            pass

    class MockMotor:
        def __init__(self):
            self.pole_number = 10 
            self.slot_number = 15 
            self.phase_number = 3
            self.i_rms = 10.0      
            self.reluctance_network = MockReluctanceNetwork()

    motor_test = MockMotor()
    drive_test = Drive(motor_test)

    # Chay thu 5 buoc de xem ket qua in ra trong console
    print("--- Debugging Initial Steps ---")
    steps_debug = 5
    test_angles = np.linspace(0, 10, steps_debug) # 0 den 10 do co hoc
    
    results = []
    for deg in test_angles:
        motor_test.reluctance_network.rotor_position = np.radians(deg)
        currents = drive_test.calculate_n_phase_currents()
        results.append(currents)
    print("--- End of Debugging Steps ---\n")

    # Tiep tuc mo phong de ve do thi (cho 2 chu ky dien = 144 do co)
    steps_plot = 400
    mech_angles_plot = np.linspace(0, 144, steps_plot)
    plot_results = []
    
    # Reset lai vi tri cho do thi
    for deg in mech_angles_plot:
        motor_test.reluctance_network.rotor_position = np.radians(deg)
        # Luu y: Lenh in trong get_drive_position se tiep tuc in ra console o day
        currents = drive_test.calculate_n_phase_currents()
        plot_results.append(currents)

    plot_results = np.array(plot_results)

    # Ve do thi
    plt.figure(figsize=(10, 5))
    colors = ['red', 'green', 'blue']
    for i in range(int(motor_test.phase_number)):
        plt.plot(mech_angles_plot, plot_results[:, i], label=f'Phase {chr(65+i)}', color=colors[i])

    plt.title(f"Debug: 3-Phase Currents (10 Poles, 15 Slots)")
    plt.xlabel("Mechanical Position (Degrees)")
    plt.ylabel("Current (A)")
    plt.axhline(0, color='black', linewidth=1)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    plt.show()