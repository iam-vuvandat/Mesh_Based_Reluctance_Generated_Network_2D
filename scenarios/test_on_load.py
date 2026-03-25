import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import math
import time
from motor_geometry.core.extract_motor_segment import extract_motor_segment
from motor_geometry.utils.create_adaptive_trapezoid_grid_for_SPM import create_adaptive_trapezoid_grid_for_SPM
from motor_geometry.models.ReluctanceNetwork import ReluctanceNetwork
from solver.core.fixed_point_iteration import fixed_point_iteration
from solver.utils.find_solver_parameter import find_solver_parameter
from motor_geometry.models.SPM import SPM



def run_single_step_on_load(spm):
    # 1. Trich xuat hinh hoc (Lay tu SPM object)
    segments = spm.extract_segments(stator_angle_offset=0, rotor_angle_offset=0)
    
    # 2. Thiet lap thong so luoi (Quality Medium)
    total_col, _, _, _, _, _, _ = find_solver_parameter(spm, n_point_plot=33)
    n_rotor_yoke, n_magnet, n_airgap, n_tooth_tip, n_tooth, n_stator_yoke = 6, 6, 5, 6, 6, 6
    
    # 3. Khoi tao luoi va ReluctanceNetwork
    grid = create_adaptive_trapezoid_grid_for_SPM(spm, n_rotor_yoke, n_magnet, n_airgap, n_tooth_tip, n_tooth, n_stator_yoke, total_col + 1)
    rn = ReluctanceNetwork(segments, grid, cyclic_type="first_dimension")
    
    # 4. Dong bo mang vao motor va tao Drive
    spm.reluctance_network = rn
    spm.create_drive()
    
    # 5. Ap dung kich tu On-load (Su dung i_rms = 20A mac dinh cua SPM)
    spm.drive.apply_winding_excitation(excitation=True)
    
    # 6. Giai buoc 0 (First Step)
    print(f"--- Simulation Start: {spm.slot_number} Slots, {spm.pole_number} Poles ---")
    print(f"Current i_rms: {spm.i_rms}A")
    
    start_time = time.perf_counter()
    rn = fixed_point_iteration(rn, first_step=True)
    solve_time = time.perf_counter() - start_time
    
    # 7. Tinh Torque Maxwell tai Air-gap
    airgap_idx = int(n_rotor_yoke + n_magnet + n_airgap // 2) + 1
    torque = rn.maxwell_stress_tensor(airgap_idx) * spm.reduce_factor
    
    print("-" * 30)
    print(f"Solving Time: {solve_time:.4f} s")
    print(f"Electromagnetic Torque: {torque:.4f} Nm")
    print("-" * 30)
    
    # 8. Hien thi ket qua
    rn.view_flux_density(show_plot=True)

if __name__ == "__main__":
    # --- KHOI TAO DOI TUONG SPM TAI DAY ---
    # Khoi tao voi thong so ban yeu cau: 15 slot, 10 cuc, i_rms = 20A
    my_motor = SPM(
        i_rms=0
    )
    
    # Chay mo phong don diem
    run_single_step_on_load(my_motor)