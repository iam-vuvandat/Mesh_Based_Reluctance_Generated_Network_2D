import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import matplotlib.pyplot as plt
import scienceplots
import numpy as np 
from ansys.utils.load_motor_cad import load_motor_cad
from ansys.core.magnetic_calculation import magnetic_calculation
from data.utils.get_waveform_nrmse import get_waveform_nrmse
from data.utils.data_helper import save, load
from tqdm import tqdm

def run():
    solve_motor_cad = False
    npoint = 10
    mesh_unit = 155

    if solve_motor_cad:
        airgap_mesh_variable = [int(x) for x in np.arange(1, npoint + 1) * mesh_unit]
        mcad = load_motor_cad(r"C:\Users\Surface\Desktop\5.mot")
        data_solved = []
        for val in airgap_mesh_variable:
            mcad.set_variable("AirgapMeshPoints_layers", val)
            mcad.set_variable("AirgapMeshPoints_mesh", val)
            data_solved.append(magnetic_calculation(mcad, show_plot=False))
        save(data001=data_solved)
    else:
        data_solved = load("data001")

    npoint = len(data_solved)
    NRMSE_error = np.zeros((9, npoint))
    for i in range(npoint):
        ref = data_solved[-1]
        curr = data_solved[i]
        NRMSE_error[-1, i] = curr.element_number
        NRMSE_error[0, i] = get_waveform_nrmse(ref.airgap_flux_density, curr.airgap_flux_density, row_index=0)
        NRMSE_error[3, i] = get_waveform_nrmse(ref.flux_linkage, curr.flux_linkage, row_index=0)
        NRMSE_error[6, i] = get_waveform_nrmse(ref.cogging_torque, curr.cogging_torque, row_index=0)
        NRMSE_error[7, i] = float(curr.total_time[0])

    save(data0056=NRMSE_error)
    avg_time = np.mean(NRMSE_error[7, :])

    plt.style.use(['science', 'no-latex'])
    plt.rcParams.update({
        'font.size': 20,
        'axes.titlesize': 30,
        'axes.labelsize': 25,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'legend.fontsize': 18,
        'font.family': 'Times New Roman'
    })

    colors = [
        '#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB', 
        '#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F', 
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', 
        '#7f7f7f', '#bcbd22', '#17becf', '#FF0000', '#0000FF', '#008000', '#000000', 
        '#FFA500', '#800080', '#FF00FF', '#808080' 
    ]
    markers = ['o', 's', '^', 'v', 'D', 'X', 'd']
    linestyles = ['-', '--', ':', '-.']

    fig, ax1 = plt.subplots(figsize=(16, 10))

    ax1.plot(NRMSE_error[-1], NRMSE_error[0], label=r'Airgap Flux Density', 
            linestyle=linestyles[0], linewidth=3.0, color=colors[7], marker=markers[0])
    ax1.plot(NRMSE_error[-1], NRMSE_error[3], label=r'Flux Linkage', 
            linestyle=linestyles[0], linewidth=3.0, color=colors[8], marker=markers[1])
    ax1.plot(NRMSE_error[-1], NRMSE_error[6], label=r'Cogging Torque', 
            linestyle=linestyles[0], linewidth=3.0, color=colors[10], marker=markers[2])

    ax1.set_xlabel(r'Element Number')
    ax1.set_ylabel(r'NRMSE ($\%$)')
    ax1.set_ylim(bottom=0)
    ax1.grid(True, which='both', linestyle='-', linewidth=0.1)

    ax2 = ax1.twinx()
    # Đã cập nhật label để hiển thị Avg Time vào Legend
    ax2.plot(NRMSE_error[-1], NRMSE_error[7], label=f'Computation Time (Average: {avg_time:.1f} s)', 
            linestyle=linestyles[0], linewidth=1.0, color=colors[27], marker=markers[4])

    for x, y in zip(NRMSE_error[-1], NRMSE_error[7]):
        ax2.text(x, y + (max(NRMSE_error[7])*0.05), f'{y:.2f}s', 
                ha='center', va='bottom', fontsize=14, fontweight='bold', color=colors[27])

    ax2.set_ylabel(r'Computation Time ($s$)')
    ax2.set_ylim(0, max(NRMSE_error[7]) * 40.0) 

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(handles=h1 + h2, labels=l1 + l2, frameon=True, loc='upper right', ncol=1)

    # Đồ thị không tiêu đề theo yêu cầu
    # plt.title(...) đã được loại bỏ

    plt.tight_layout()
    plt.show()