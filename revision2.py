from system.core.setup import setup 
setup()
from data.utils.data_helper import load
import matplotlib.pyplot as plt
import scienceplots
import numpy as np
from solver.utils.analyze_fourier_array import analyze_fourier_array

# --- Cấu hình hiển thị ---
hide_title = True

plot_airgap_flux_density = True
plot_flux_linkage = True
plot_back_emf_phase = True 
plot_cogging_torque = True
plot_mesh_fem = True
plot_mesh_rn  = True
plot_var_airgap = True
plot_var_magthick = True

# Cấu hình phân tích hài
max_harmonic = 15
include_zero = False

plt.style.use(['science', 'no-latex'])
plt.rcParams.update({
    'font.size': 20,         
    'axes.titlesize': 30,     
    'axes.labelsize': 25,     
    'xtick.labelsize': 18,     
    'ytick.labelsize': 18,     
    'legend.fontsize': 18,    
})

colors = [
    '#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB',
    '#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F',
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', 
    '#7f7f7f', '#bcbd22', '#17becf', '#FF0000', '#0000FF', '#008000', '#000000', 
    '#FFA500', '#800080', '#FF00FF', '#808080'
]
markers = ['o', 's', '^', 'v', 'D', 'X']
linestyles = ['-', '--', ':']

def print_stats(name, labels, data_array):
    print(f"\n{'='*10} {name} STATISTICS {'='*10}")
    for i, label in enumerate(labels):
        signal = data_array[i]
        peak = np.max(np.abs(signal))
        avg = np.mean(signal)
        rms = np.sqrt(np.mean(np.square(signal)))
        print(f"[{label}] Peak: {peak:.4f} | Avg: {avg:.4f} | RMS: {rms:.4f}")

if plot_airgap_flux_density == True:
    fem_data = load("fem1")
    rn_data  = load("rn1")

    airgap_data_fem = fem_data.airgap_flux_density
    airgap_data_rn  = rn_data.airgap_flux_density
    
    labels_b = ["|B|", "Br", "Bt"]
    print_stats("AIRGAP FLUX DENSITY (FEM)", labels_b, airgap_data_fem)
    print_stats("AIRGAP FLUX DENSITY (MBGRN)", labels_b, airgap_data_rn)

    # --- Airgap Waveform Plot ---
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.plot(airgap_data_fem[-1], airgap_data_fem[0], label=r'$|B|$-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[0], markevery=20, color=colors[7])
    ax.plot(airgap_data_fem[-1], airgap_data_fem[1], label=r'$B_r$-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[1], markevery=20, color=colors[8])
    ax.plot(airgap_data_fem[-1], airgap_data_fem[2], label=r'$B_t$-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[2], markevery=20, color=colors[10])

    ax.plot(airgap_data_rn[-1], airgap_data_rn[0], label=r'$|B|$-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[0], markevery=20, color=colors[7])
    ax.plot(airgap_data_rn[-1], airgap_data_rn[1], label=r'$B_r$-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[1], markevery=20, color=colors[8])
    ax.plot(airgap_data_rn[-1], airgap_data_rn[2], label=r'$B_t$-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[2], markevery=20, color=colors[10])

    ax.set_xlabel(r'Position ($Deg$)')
    ax.set_ylabel(r'Flux density ($T$)')
    if not hide_title: ax.set_title(r'Comparison of Airgap Flux Density')
    ax.legend(frameon=True, loc='best', ncol=2)
    ax.grid(True, which='both', linestyle='-', linewidth=0.05)
    plt.show()

    # --- Airgap Harmonics (Grouped Br and Bt) ---
    h_fem = analyze_fourier_array(airgap_data_fem, max_harmonic, include_zero_order=include_zero)
    h_rn = analyze_fourier_array(airgap_data_rn, max_harmonic, include_zero_order=include_zero)
    
    fig_h, ax_h = plt.subplots(figsize=(20, 10))
    x = h_fem[-1]
    width = 0.2
    
    ax_h.bar(x - 1.5*width, h_fem[1], width, label=r'$B_r$-FEM', color=colors[8], alpha=0.4)
    ax_h.bar(x - 0.5*width, h_rn[1],  width, label=r'$B_r$-MBGRN', color=colors[8])
    ax_h.bar(x + 0.5*width, h_fem[2], width, label=r'$B_t$-FEM', color=colors[10], alpha=0.4)
    ax_h.bar(x + 1.5*width, h_rn[2],  width, label=r'$B_t$-MBGRN', color=colors[10])
    
    ax_h.set_xlabel('Harmonic Order')
    ax_h.set_ylabel('Amplitude (T)')
    if not hide_title: ax_h.set_title(r'Harmonic Spectrum of Airgap Flux Density ($B_r$ & $B_t$)')
    ax_h.set_xticks(x)
    ax_h.legend(ncol=2)
    ax_h.grid(axis='y', linestyle='--', alpha=0.3)
    plt.show()

if plot_flux_linkage == True:
    flux_linkage_fem = fem_data.flux_linkage
    flux_linkage_rn  = rn_data.flux_linkage
    
    labels_f = ["Phase A", "Phase B", "Phase C"]
    print_stats("FLUX LINKAGE (FEM)", labels_f, flux_linkage_fem)
    print_stats("FLUX LINKAGE (MBGRN)", labels_f, flux_linkage_rn)

    # --- Flux Linkage Waveform ---
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.plot(flux_linkage_fem[-1], flux_linkage_fem[0], label=r'Phase A-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[0], markevery=5, color=colors[7])
    ax.plot(flux_linkage_fem[-1], flux_linkage_fem[1], label=r'Phase B-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[1], markevery=5, color=colors[8])
    ax.plot(flux_linkage_fem[-1], flux_linkage_fem[2], label=r'Phase C-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[2], markevery=5, color=colors[10])
    ax.plot(flux_linkage_rn[-1], flux_linkage_rn[0], label=r'Phase A-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[0], markevery=5, color=colors[7])
    ax.plot(flux_linkage_rn[-1], flux_linkage_rn[1], label=r'Phase B-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[1], markevery=5, color=colors[8])
    ax.plot(flux_linkage_rn[-1], flux_linkage_rn[2], label=r'Phase C-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[2], markevery=5, color=colors[10])

    ax.set_xlabel(r'Rotor Position ($Deg$)')
    ax.set_ylabel(r'Flux Linkage ($Wb$)')
    if not hide_title: ax.set_title(r'Comparison of Flux Linkage')
    ax.legend(frameon=True, loc='best', ncol=1)
    ax.grid(True, which='both', linestyle='-', linewidth=0.05)
    plt.show()

    h_fem = analyze_fourier_array(flux_linkage_fem, max_harmonic, include_zero_order=include_zero)
    h_rn = analyze_fourier_array(flux_linkage_rn, max_harmonic, include_zero_order=include_zero)
    
    fig_h, ax_h = plt.subplots(figsize=(16, 8))
    width_fl = 0.35
    ax_h.bar(h_fem[-1] - width_fl/2, h_fem[0], width_fl, label='Phase A-FEM', color=colors[7], alpha=0.4)
    ax_h.bar(h_rn[-1] + width_fl/2, h_rn[0],  width_fl, label='Phase A-MBGRN', color=colors[7])
    ax_h.set_xlabel('Harmonic Order')
    ax_h.set_ylabel('Amplitude (Wb)')
    if not hide_title: ax_h.set_title('Harmonic Spectrum of Flux Linkage (Phase A)')
    ax_h.set_xticks(h_fem[-1])
    ax_h.legend()
    plt.show()

if plot_back_emf_phase == True:
    back_emf_phase_fem = fem_data.back_emf_phase
    back_emf_phase_rn  = rn_data.back_emf_phase
    
    labels_e = ["Phase A", "Phase B", "Phase C"]
    print_stats("BACK EMF (FEM)", labels_e, back_emf_phase_fem)
    print_stats("BACK EMF (MBGRN)", labels_e, back_emf_phase_rn)

    # --- Back EMF Waveform ---
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.plot(back_emf_phase_fem[-1], back_emf_phase_fem[0], label=r'Phase A-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[0], markevery=5, color=colors[7])
    ax.plot(back_emf_phase_fem[-1], back_emf_phase_fem[1], label=r'Phase B-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[1], markevery=5, color=colors[8])
    ax.plot(back_emf_phase_fem[-1], back_emf_phase_fem[2], label=r'Phase C-FEM', linestyle=linestyles[1], linewidth=1.0, marker=markers[2], markevery=5, color=colors[10])
    ax.plot(back_emf_phase_rn[-1], back_emf_phase_rn[0], label=r'Phase A-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[0], markevery=5, color=colors[7])
    ax.plot(back_emf_phase_rn[-1], back_emf_phase_rn[1], label=r'Phase B-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[1], markevery=5, color=colors[8])
    ax.plot(back_emf_phase_rn[-1], back_emf_phase_rn[2], label=r'Phase C-MBGRN', linestyle=linestyles[0], linewidth=3.0, marker=markers[2], markevery=5, color=colors[10])

    ax.set_xlabel(r'Rotor Position ($Deg$)')
    ax.set_ylabel(r'Back EMF ($V$)')
    if not hide_title: ax.set_title(r'Comparison of Back EMF (Phase)')
    ax.legend(frameon=True, loc='lower right', ncol=1)
    ax.grid(True, which='both', linestyle='-', linewidth=0.05)
    plt.show()

    h_fem = analyze_fourier_array(back_emf_phase_fem, max_harmonic, include_zero_order=include_zero)
    h_rn = analyze_fourier_array(back_emf_phase_rn, max_harmonic, include_zero_order=include_zero)
    
    fig_h, ax_h = plt.subplots(figsize=(16, 8))
    width_be = 0.35
    ax_h.bar(h_fem[-1] - width_be/2, h_fem[0], width_be, label='Phase A-FEM', color=colors[7], alpha=0.4)
    ax_h.bar(h_rn[-1] + width_be/2, h_rn[0],  width_be, label='Phase A-MBGRN', color=colors[7])
    ax_h.set_xlabel('Harmonic Order')
    ax_h.set_ylabel('Amplitude (V)')
    if not hide_title: ax_h.set_title('Harmonic Spectrum of Back EMF (Phase A)')
    ax_h.set_xticks(h_fem[-1])
    ax_h.legend()
    plt.show()

if plot_cogging_torque == True:
    cogging_fem = fem_data.cogging_torque
    cogging_rn  = rn_data.torque_maxwell_stress_tensor
    
    print_stats("COGGING TORQUE (FEM)", ["Torque"], cogging_fem)
    print_stats("COGGING TORQUE (MBGRN)", ["Torque"], cogging_rn)

    # --- Cogging Torque Waveform ---
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.plot(cogging_fem[-1], cogging_fem[0], label=r'Cogging Torque-FEM', linestyle=linestyles[1], linewidth=1.0, color=colors[7])
    ax.plot(cogging_rn[-1], cogging_rn[0], label=r'Cogging Torque-MBGRN', linestyle=linestyles[0], linewidth=3.0, color=colors[8])
    ax.set_xlabel(r'Rotor Position ($Deg$)')
    ax.set_ylabel(r'Torque ($N.m$)')
    if not hide_title: ax.set_title(r'Comparison of Cogging Torque')
    ax.legend(frameon=True, loc='lower right', ncol=1)
    ax.grid(True, which='both', linestyle='-', linewidth=0.05)
    plt.show()

    h_fem = analyze_fourier_array(cogging_fem, max_harmonic, include_zero_order=include_zero)
    h_rn = analyze_fourier_array(cogging_rn, max_harmonic, include_zero_order=include_zero)
    
    fig_h, ax_h = plt.subplots(figsize=(16, 8))
    width_ct = 0.35
    ax_h.bar(h_fem[-1] - width_ct/2, h_fem[0], width_ct, label='FEM', color=colors[7], alpha=0.4)
    ax_h.bar(h_rn[-1] + width_ct/2, h_rn[0],  width_ct, label='MBGRN', color=colors[8])
    ax_h.set_xlabel('Harmonic Order')
    ax_h.set_ylabel('Amplitude (N.m)')
    if not hide_title: ax_h.set_title('Harmonic Spectrum of Cogging Torque')
    ax_h.set_xticks(h_fem[-1])
    ax_h.legend()
    plt.show()

if plot_mesh_fem:
    from scenarios.simulate_with_mesh_variable import run
    run()
if plot_mesh_rn:
    from scenarios.rn_simulate_with_mesh_variable import run
    run()
if plot_var_airgap:
    from scenarios.simulate_with_airgap_variable import run
    run()
if plot_var_magthick:
    from scenarios.simulate_with_magnet_thicknees_variable import run
    run()