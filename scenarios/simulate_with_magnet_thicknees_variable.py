import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

import matplotlib.pyplot as plt
import scienceplots
import numpy as np 
from ansys.utils.load_motor_cad import load_motor_cad
from ansys.core.magnetic_calculation import magnetic_calculation
from motor_geometry.models.SPM import SPM
from data.utils.get_waveform_nrmse import get_waveform_nrmse
from data.utils.data_helper import save, load
from tqdm import tqdm

def run():
    # ==============================================================================
    # --- CONFIGURATION (User frequently adjusts these) ---
    # ==============================================================================
    # --- Simulation & Data ---
    n_point = 20
    plot_density = 1 
    magnet_thickness_min = 0.5
    magnet_thickness_max = 4.0
    mcad_file_path = r"C:\Users\Surface\Desktop\5.mot"

    run_motor_cad = False
    run_rn = False

    # --- Plotting Scale (ylim multipliers) ---
    nrmse_scale_factor = 2.2      # Tỉ lệ scale trục NRMSE (ax1)
    time_scale_factor = 1.5       # Tỉ lệ scale trục Computation Time (ax2)
    time_axis_bottom_offset = -15 # Offset đáy trục time để tránh dính đường 0%

    # --- Label settings ---
    fem_text_offset = 0.02        # Khoảng cách nhãn FEM so với marker
    rn_text_offset = 0.02         # Khoảng cách nhãn RN so với marker
    text_va = 'bottom'            # Căn lề dọc nhãn ('bottom' để đẩy chữ lên trên)
    time_label_fontsize = 9       # Kích thước số trên đường thời gian
    legend_loc = 'upper left'     # Vị trí bảng chú giải
    # ==============================================================================


    magnet_thickness_variable = np.linspace(magnet_thickness_min, magnet_thickness_max, n_point)

    if run_motor_cad: 
        mcad = load_motor_cad(mcad_file_path)
        fem_data = []
        for i in range(n_point):
            mcad.set_variable("Magnet_Thickness", magnet_thickness_variable[i])
            fem_data.append(magnetic_calculation(mcad, show_plot=False))
        save(data_magnet_thickness_fem = fem_data)
    else:
        fem_data = load("data_magnet_thickness_fem")

    if run_rn:
        rn_data = []
        for i in tqdm(range(n_point), desc="Analyzing Magnet Thickness", ncols=100, leave=False):
            spm = SPM(magnet_thickness=magnet_thickness_variable[i] * 1e-3)
            rn_data.append(spm.solve_open_circuit(show_plot=False, debug=False, quality="medium"))
        save(data_magnet_thickness_rn = rn_data)
    else:
        rn_data = load("data_magnet_thickness_rn")

    field_name = ["Air gap flux density", "airgap_flux_density_radial", "airgap_flux_density_tangential",
                    "Flux linkage", "Back EMF phase", "back_emf_line", "cogging_coenergy",
                    "Cogging torque", "FEM computation time", "RN computation time"]

    plot_data = np.zeros((11, n_point))
    for i in range(n_point):
        plot_data[0, i] = get_waveform_nrmse(fem_data[i].airgap_flux_density, rn_data[i].airgap_flux_density, row_index=0)
        plot_data[1, i] = get_waveform_nrmse(fem_data[i].airgap_flux_density, rn_data[i].airgap_flux_density, row_index=1)
        plot_data[2, i] = get_waveform_nrmse(fem_data[i].airgap_flux_density, rn_data[i].airgap_flux_density, row_index=2)
        plot_data[3, i] = get_waveform_nrmse(fem_data[i].flux_linkage, rn_data[i].flux_linkage)
        plot_data[4, i] = get_waveform_nrmse(fem_data[i].back_emf_phase, rn_data[i].back_emf_phase)
        plot_data[5, i] = get_waveform_nrmse(fem_data[i].back_emf_line, rn_data[i].back_emf_line)
        plot_data[6, i] = get_waveform_nrmse(fem_data[i].cogging_torque, rn_data[i].cogging_torque)
        plot_data[7, i] = get_waveform_nrmse(fem_data[i].cogging_torque, rn_data[i].torque_maxwell_stress_tensor)
        plot_data[8, i] = fem_data[i].total_time[0]
        plot_data[9, i] = rn_data[i].total_time
        plot_data[10, i] = magnet_thickness_variable[i]

    display_data = plot_data[:, ::plot_density]
    avg_time_fem = np.mean(plot_data[8, :])
    avg_time_rn = np.mean(plot_data[9, :])
    speed_up = avg_time_fem / avg_time_rn

    # --- Plotting Style ---
    plt.style.use(['science', 'no-latex'])
    plt.rcParams.update({
        'font.size': 20,
        'axes.labelsize': 25,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'legend.fontsize': 18,
        'font.family': 'Times New Roman'
    })

    colors = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB', 
                '#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F', '#000000']
    markers = ['o', 's', '^', 'v', 'D', 'X', 'd']

    fig, ax1 = plt.subplots(figsize=(16, 10))
    skip_indices = [1, 2, 5, 6]
    plot_index = 0
    max_nrmse_val = 0

    for i in range(8):
        if i in skip_indices: continue
        ax1.plot(display_data[10, :], display_data[i, :], linestyle='-',
                    marker=markers[plot_index % len(markers)], markersize=8, linewidth=3.0,
                    color=colors[7 + plot_index], label=field_name[i])
        max_nrmse_val = max(max_nrmse_val, np.max(display_data[i, :]))
        plot_index += 1

    ax1.set_xlabel(r'Magnet Thickness ($mm$)')
    ax1.set_ylabel(r'NRMSE ($\%$)')
    ax1.set_ylim(0, max_nrmse_val * nrmse_scale_factor)
    ax1.grid(True, which='both', linestyle='-', linewidth=0.1)

    ax2 = ax1.twinx()

    # Plot Time Curves
    ax2.plot(display_data[10, :], display_data[8, :], color='black', linestyle='-', 
                marker=markers[3], markersize=8, linewidth=1.0, label=f'FEM Time (Average: {avg_time_fem:.2f} s)')

    ax2.plot(display_data[10, :], display_data[9, :], color='black', linestyle='-', 
                marker=markers[6], markersize=8, linewidth=1.0, label=f'RN Time (Average: {avg_time_rn:.4f} s, {speed_up:.1f}x faster)')

    # Text Annotations
    max_time_fem = max(display_data[8, :])
    for x, y_fem, y_rn in zip(display_data[10, :], display_data[8, :], display_data[9, :]):
        # Bỏ chữ 's' và chỉnh fontsize nhỏ hơn
        ax2.text(x, y_fem + (max_time_fem * fem_text_offset), f'{y_fem:.1f}', 
                    ha='center', va=text_va, fontsize=time_label_fontsize, fontweight='bold', color='black')
        ax2.text(x, y_rn + (max_time_fem * rn_text_offset), f'{y_rn:.3f}', 
                    ha='center', va=text_va, fontsize=time_label_fontsize, fontweight='bold', color='black')

    ax2.set_ylabel(r'Computation Time ($s$)')
    ax2.set_ylim(time_axis_bottom_offset, max_time_fem * time_scale_factor)

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(handles=h1 + h2, labels=l1 + l2, frameon=True, loc=legend_loc, ncol=1)

    plt.tight_layout()
    plt.show()

