"""
MAIN_CirculationModelSimulation
This code simulates pressure-volume behavior of left and right ventricles
coupled to a circuit model of the systemic and pulmonary circulations
This is a function to simulate the pump function of the heart and its coupling to the circulation. It is
based on a series of papers by Daniel Burkhoff (two prominent references are Santamore WP and Burkhoff D, Am
J Physiol 1991 and Burkhoff D and Tyberg JV, Am J Physiol 1993).
Designed in MATLAB by Colleen Witzenburg February 2017
Adapted in Python by Ashley Hiebing September 2025

Volume and Pressure Compartment Designations
    Column  Compartment
    0       pulmonary veins
    1       left ventricle - surviving myocardium
    2       systemic arteries
    3       systemic veins
    4       right ventricle
    5       pulmonary arteries
    6       left ventricle - infarct scar
"""
from set_initial_conditions import set_initial_conditions
from simulate_heart_beat import simulate_heart_beat
from plotting_outputs import plotting_outputs
import numpy as np

# Load input parameters and initialize vectors
Volumes, time_vector, tes, ventricles, resistances, capacitances = set_initial_conditions()

# Simulate heart beat
Volumes, Pressures, Valves, Flows = simulate_heart_beat(resistances, capacitances, ventricles, time_vector, tes, Volumes)

# Calculating outputs
SBP = max(Pressures[:, 2])
DBP = min(Pressures[:, 2])
MAP = (1/3) * SBP + (2/3) * DBP # mean arterial pressure (mmHg)
SV = max(Volumes[:, 1]) - min(Volumes[:, 1]) # stroke volume (ml)
CO = SV * (1 / max(time_vector) * 60) * (1/1000) # cardiac output (L/min)
max_dpdt = max(np.diff(Pressures[:, 1]) / np.diff(time_vector))
row_MV_closes = np.nonzero(np.diff(Valves[:, 0]) == -1)
EDP = Pressures[row_MV_closes, 1] # end diastolic pressure (mmHg)

print("Mean arterial pressure: " + str(round(MAP,2)) + " mmHg")
print("Stroke volume: " + str(round(SV,2)) + " ml")
print("Cardiac output: " + str(round(CO,2)) + " L/min")
print("Max dP/dt: " + str(round(max_dpdt,2)) + " mmHg/s")
print("End-diastolic pressure: " + str(round(EDP.item(),2)) + " mmHg")

# Plotting
plotting_outputs(ventricles, Volumes, Pressures, Valves, Flows, time_vector)