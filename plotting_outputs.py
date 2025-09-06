"""
plotting_outputs.py
Plots pressure volume loops, valve opening/closing, and flows over time
"""

import numpy as np
import matplotlib.pyplot as plt

def plotting_outputs(ventricles, Volumes, Pressures, Valves, Flows, time_vector):

    #----Pressure Volume Loops----
    v = np.arange(0, 101) # for plotting ESPVR and EDPVR

    fig1, axs1 = plt.subplots(1, 2, figsize=(12, 5))

    # Subplot 1: Left ventricle
    A_lv = ventricles[0, 0]
    B_lv = ventricles[0, 1]
    Ees_lv = ventricles[0, 2]
    V0_lv = ventricles[0, 3]

    # ESPVR: End-systolic pressure-volume relationship (linear)
    espvr_lv = Ees_lv * (v - V0_lv)

    # EDPVR: End-diastolic pressure-volume relationship (exponential)
    edpvr_lv = B_lv * np.exp(A_lv * (v - V0_lv)) - B_lv

    axs1[0].plot(v, espvr_lv, '--k', label='ESPVR')
    axs1[0].plot(v, edpvr_lv, '--k', label='EDPVR')
    axs1[0].plot(Volumes[:, 1], Pressures[:, 1], '-', linewidth=2, label='LV PV Loop')

    axs1[0].set_xlabel('LV Volume (ml)')
    axs1[0].set_ylabel('LV Pressure (mmHg)')
    axs1[0].set_xlim([0, 1.1 * np.max(Volumes[:, 1])])
    axs1[0].set_ylim([0, 1.1 * np.max(Pressures[:, 1])])

    # Subplot 2: Right ventricle
    A_rv = ventricles[1, 0]
    B_rv = ventricles[1, 1]
    Ees_rv = ventricles[1, 2]
    V0_rv = ventricles[1, 3]

    # ESPVR: End-systolic pressure-volume relationship (linear)
    espvr_rv = Ees_rv * (v - V0_rv)

    # EDPVR: End-diastolic pressure-volume relationship (exponential)
    edpvr_rv = B_rv * np.exp(A_rv * (v - V0_rv)) - B_rv

    axs1[1].plot(v, espvr_rv, '--k', label='ESPVR')
    axs1[1].plot(v, edpvr_rv, '--k', label='EDPVR')
    axs1[1].plot(Volumes[:, 4], Pressures[:, 4], '-', linewidth=2, label='RV PV Loop')

    axs1[1].set_xlabel('RV Volume (ml)')
    axs1[1].set_ylabel('RV Pressure (mmHg)')
    axs1[1].set_xlim([0, 1.1 * np.max(Volumes[:, 4])])
    axs1[1].set_ylim([0, 1.1 * np.max(Pressures[:, 4])])

    plt.tight_layout()

    #----Pressure and Volume vs Time----
    valve_change = np.diff(Valves, axis=0)  # MV, AV, TV, PV
    row_MV_opens = np.nonzero(valve_change[:, 0] == 1)
    row_MV_closes = np.nonzero(valve_change[:, 0] == -1)
    row_AV_opens = np.nonzero(valve_change[:, 1] == 1)
    row_AV_closes = np.nonzero(valve_change[:, 1] == -1)
    row_TV_opens = np.nonzero(valve_change[:, 2] == 1)
    row_TV_closes = np.nonzero(valve_change[:, 2] == -1)
    row_PV_opens = np.nonzero(valve_change[:, 3] == 1)
    row_PV_closes = np.nonzero(valve_change[:, 3] == -1)

    # Left side pressures
    fig2, axs2 = plt.subplots(2, 2, figsize=(12, 8))

    ax = axs2[0, 0] # top left corner

    # Plot vertical lines at valve event times
    for row in row_AV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='AV opens' if row == row_AV_opens[0] else "")
    for row in row_AV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='AV closes' if row == row_AV_closes[0] else "")
    for row in row_MV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='MV opens' if row == row_MV_opens[0] else "")
    for row in row_MV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='MV closes' if row == row_MV_closes[0] else "")

    # Plot pressure curves: PV, LV, SA
    ax.plot(time_vector, Pressures[:, 0], '-', linewidth=2, label='Pulmonary Veins')
    ax.plot(time_vector, Pressures[:, 1], '-', linewidth=2, label='LV')
    ax.plot(time_vector, Pressures[:, 2], '-', linewidth=2, label='Systemic Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pressure (mmHg)')
    ax.legend()

    # Right side pressures
    ax = axs2[0, 1]  # top right corner

    # Plot vertical lines at valve event times
    for row in row_PV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='PV opens' if row == row_PV_opens[0] else "")
    for row in row_PV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='PV closes' if row == row_PV_closes[0] else "")
    for row in row_TV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='TV opens' if row == row_TV_opens[0] else "")
    for row in row_TV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='TV closes' if row == row_TV_closes[0] else "")

    # Plot pressure curves: SV, RV, SPA
    ax.plot(time_vector, Pressures[:, 3], '-', linewidth=2, label='Systemic Veins')
    ax.plot(time_vector, Pressures[:, 4], '-', linewidth=2, label='RV')
    ax.plot(time_vector, Pressures[:, 5], '-', linewidth=2, label='Pulmonary Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Pressure (mmHg)')
    ax.legend()

    # Left side volumes
    ax = axs2[1, 0]  # bottom left corner

    # Plot vertical lines at valve event times
    for row in row_AV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='AV opens' if row == row_AV_opens[0] else "")
    for row in row_AV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='AV closes' if row == row_AV_closes[0] else "")
    for row in row_MV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='MV opens' if row == row_MV_opens[0] else "")
    for row in row_MV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='MV closes' if row == row_MV_closes[0] else "")

    # Plot volume curves: PV, LV, SA
    ax.plot(time_vector, Volumes[:, 0], '-', linewidth=2, label='Pulmonary Veins')
    ax.plot(time_vector, Volumes[:, 1], '-', linewidth=2, label='LV')
    ax.plot(time_vector, Volumes[:, 2], '-', linewidth=2, label='Systemic Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Volume (ml)')
    ax.legend()

    # Right side volumes
    ax = axs2[1, 1]  # bottom right corner

    # Plot vertical lines at valve event times
    for row in row_PV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='PV opens' if row == row_PV_opens[0] else "")
    for row in row_PV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='PV closes' if row == row_PV_closes[0] else "")
    for row in row_TV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='TV opens' if row == row_TV_opens[0] else "")
    for row in row_TV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='TV closes' if row == row_TV_closes[0] else "")

    # Plot volume curves: SV, RV, SPA
    ax.plot(time_vector, Volumes[:, 3], '-', linewidth=2, label='Systemic Veins')
    ax.plot(time_vector, Volumes[:, 4], '-', linewidth=2, label='RV')
    ax.plot(time_vector, Volumes[:, 5], '-', linewidth=2, label='Pulmonary Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Volume (ml)')
    ax.legend()

    #----Flows vs Time----

    # Left side flows
    fig3, axs3 = plt.subplots(1, 2, figsize=(12, 8))

    ax = axs3[0]  # left

    # Plot vertical lines at valve event times
    for row in row_AV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='AV opens' if row == row_AV_opens[0] else "")
    for row in row_AV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='AV closes' if row == row_AV_closes[0] else "")
    for row in row_MV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='MV opens' if row == row_MV_opens[0] else "")
    for row in row_MV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='MV closes' if row == row_MV_closes[0] else "")

    # Plot flow curves: PV, LV, SA
    ax.plot(time_vector, Flows[:, 0], '-', linewidth=2, label='Pulmonary Veins')
    ax.plot(time_vector, Flows[:, 1], '-', linewidth=2, label='LV')
    ax.plot(time_vector, Flows[:, 2], '-', linewidth=2, label='Systemic Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Flow (ml/s)')
    ax.legend()

    # Right side flows
    ax = axs3[1]  # right

    # Plot vertical lines at valve event times
    for row in row_PV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='black', label='PV opens' if row == row_PV_opens[0] else "")
    for row in row_PV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='black', label='PV closes' if row == row_PV_closes[0] else "")
    for row in row_TV_opens:
        ax.axvline(time_vector[row], linestyle='--', color='gray', label='TV opens' if row == row_TV_opens[0] else "")
    for row in row_TV_closes:
        ax.axvline(time_vector[row], linestyle='-', color='gray', label='TV closes' if row == row_TV_closes[0] else "")

    # Plot flow curves: SV, RV, SPA
    ax.plot(time_vector, Flows[:, 3], '-', linewidth=2, label='Systemic Veins')
    ax.plot(time_vector, Flows[:, 4], '-', linewidth=2, label='RV')
    ax.plot(time_vector, Flows[:, 5], '-', linewidth=2, label='Pulmonary Arteries')

    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Flow (ml/s)')
    ax.legend()

    plt.show()