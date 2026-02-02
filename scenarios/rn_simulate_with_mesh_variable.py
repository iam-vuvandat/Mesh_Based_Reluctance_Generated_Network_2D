import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
import matplotlib.pyplot as plt
import scienceplots
import numpy as np 
from motor_geometry.models.SPM import SPM
from data.utils.get_waveform_nrmse import get_waveform_nrmse
from data.utils.data_helper import save, load
from tqdm import tqdm

solve_analisys = False

npoint = 10
quality_begin = 0
quality = [int(i + quality_begin) for i in range(npoint)]

spm = SPM()
if solve_analisys == True: 
    data_solved = []
    for i in quality:
        data_solved.append(spm.solve_open_circuit(
                            solve_airgap=True,
                            solve_flux_linkage=True,
                            solve_back_emf_phase=True,
                            solve_back_emf_line=True,
                            solve_cogging_torque=True,
                            show_plot=False,
                            debug=False,
                            save_data=True,
                            quality=i,
                            angle_unit="degree"))
    save(data_9827=data_solved)
else:
    data_solved = load("data_9827")

nsolved = len(data_solved)
NRMSE_error = np.zeros((9, nsolved))
ref = data_solved[-1]

for idx in tqdm(range(nsolved), desc="Đang tính NRMSE"):
    current = data_solved[idx]
    NRMSE_error[-1, idx] = current.element_number
    NRMSE_error[0, idx] = get_waveform_nrmse(ref.airgap_flux_density, current.airgap_flux_density, row_index=0)
    NRMSE_error[1, idx] = get_waveform_nrmse(ref.airgap_flux_density, current.airgap_flux_density, row_index=1)
    NRMSE_error[2, idx] = get_waveform_nrmse(ref.airgap_flux_density, current.airgap_flux_density, row_index=2)
    NRMSE_error[3, idx] = get_waveform_nrmse(ref.flux_linkage, current.flux_linkage, row_index=0)
    NRMSE_error[4, idx] = get_waveform_nrmse(ref.back_emf_phase, current.back_emf_phase, row_index=0)
    NRMSE_error[5, idx] = get_waveform_nrmse(ref.back_emf_line, current.back_emf_line, row_index=0)
    NRMSE_error[6, idx] = get_waveform_nrmse(ref.torque_maxwell_stress_tensor, current.torque_maxwell_stress_tensor, row_index=0)
    NRMSE_error[7, idx] = float(current.total_time)

save(data_9973=NRMSE_error)
element_numbers = NRMSE_error[-1]
total_time = NRMSE_error[7]
avg_time = np.mean(total_time)

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

signals_to_plot = [0, 3, 6]
labels = {0: "Airgap flux density", 3: "Flux linkage", 6: "Cogging torque"}
marker_styles = {0: ('o', '-'), 3: ('^', '-'), 6: ('s', '-')}
signal_colors = {0: colors[7], 3: colors[8], 6: colors[10]}

for i in signals_to_plot:
    marker, linestyle = marker_styles[i]
    color = signal_colors[i]
    ax1.plot(
        element_numbers,
        NRMSE_error[i],
        marker=marker,
        linestyle=linestyle,
        color=color,
        linewidth=3.0,
        markersize=7,
        label=labels[i]
    )

ax1.set_xlabel(r'Element Number')
ax1.set_ylabel(r'NRMSE ($\%$)')
ax1.set_ylim(bottom=0)
ax1.grid(True, which='both', linestyle='-', linewidth=0.1)

ax2 = ax1.twinx()
ax2.plot(
    element_numbers,
    total_time,
    label=f'Computation Time (Average: {avg_time:.1f} s)',
    marker=markers[6],
    linestyle=linestyles[0],
    linewidth=1.0,
    markersize=6,
    color=colors[27]
)

for x, y in zip(element_numbers, total_time):
    ax2.text(x, y + (max(total_time) * 0.05), f'{y:.3f} s', 
             ha='center', va='bottom', fontsize=14, fontweight='bold', color=colors[27])

ax2.set_ylabel(r'Computation Time ($s$)')
ax2.set_ylim(0, max(total_time) * 2.5)

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(handles=h1 + h2, labels=l1 + l2, frameon=True, loc='upper right', ncol=1)

plt.tight_layout()
plt.show()