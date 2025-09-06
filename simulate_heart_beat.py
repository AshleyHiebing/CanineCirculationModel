"""
simulate_heart_beat.py
Simulates a cardiac cycle, calculating changes in volumes and pressures within compartments
"""
import numpy as np
from DogPVSimulation_6Comp_Python.rk4 import rk4
from DogPVSimulation_6Comp_Python.calculate_pressures import calculate_pressures

def simulate_heart_beat(resistances, capacitances, ventricles, time_vector, tes, Volumes):

    # Determine constants for circulation model
    step_size = time_vector[1] - time_vector[0]
    is_transient_state = 1
    cutoff = 0.1
    nIterations = 0
    
    # Initialize pressure array
    Pressures = np.zeros((np.shape(Volumes)[0],6))

    # Set end volume to be same as initial
    Volumes[-1, :] = Volumes[0, :]

    while is_transient_state:
        nIterations = nIterations + 1
        Volumes[0, :] = Volumes[-1, :]
        Pressures[0, :] = calculate_pressures(Volumes[0, :], Pressures[0, :], capacitances, ventricles, 0)

        # iteratively solve for volume and pressure throughout cardiac cycle
        for i in range(1,len(time_vector)):
            current_volumes = Volumes[i - 1, :]
            current_time = time_vector[i]
            current_pressures = Pressures[i - 1, :]
            Volumes[i, :], Pressures[i, :] = rk4(current_volumes, current_pressures, resistances, capacitances, ventricles,
                                                 step_size, current_time, tes)
        # Calculate if steady state has occurred
        absolute_err = abs(Volumes[-1, :] - Volumes[0, :])
        out_of_range = absolute_err > cutoff
        nOut_of_range = np.count_nonzero(out_of_range)
        is_transient_state = nOut_of_range >= 1
        print("SS iteration #" + str(nIterations) + "    Absolute error: " + str(absolute_err))

        # if steady state can't be reached, display warning
        if nIterations > 99:
            print("ERROR: SS iterations > 100, check cutoff")
            break

    # determine if valves are open or closed
    Valves = np.zeros((np.shape(Volumes)[0],4))
    Valves[:, 0] = Pressures[:, 0] > Pressures[:, 1] # MV
    Valves[:, 1] = Pressures[:, 1] > Pressures[:, 2] # AV
    Valves[:, 2] = Pressures[:, 3] > Pressures[:, 4] # TV
    Valves[:, 3] = Pressures[:, 4] > Pressures[:, 5] # PV

    # calculate flows between compartments
    Flows = np.zeros((np.shape(Volumes)[0], 6))
    Flows[:, 0] = (Pressures[:, 5] - Pressures[:, 0]) / resistances[5] # from PA to PV
    Flows[:, 1] = (Pressures[:, 0] - Pressures[:, 1]) / resistances[0] * (Pressures[:, 0] > Pressures[:, 1])  # from PV to LV
    Flows[:, 2] = (Pressures[:, 1] - Pressures[:, 2]) / resistances[1] * (Pressures[:, 1] > Pressures[:, 2]) # from LV to SA
    Flows[:, 3] = (Pressures[:, 2] - Pressures[:, 3]) / resistances[2]  # from SA to SV
    Flows[:, 4] = (Pressures[:, 3] - Pressures[:, 4]) / resistances[3] * (Pressures[:, 3] > Pressures[:, 4])  # from SV to RV
    Flows[:, 5] = (Pressures[:, 4] - Pressures[:, 5]) / resistances[4] * (Pressures[:, 4] > Pressures[:, 5])  # from RV to PA

    return Volumes, Pressures, Valves, Flows