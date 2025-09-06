# CanineCirculationModel
Replicates circulatory model from Daniel Burkhoff (see Santamore WP and Burkhoff D, Am J Physiol 1991 and Burkhoff D and Tyberg JV, Am J Physiol 1993). Model originally developed in MATLAB by Colleen Witzenburg, adapted to Python by Ashley Hiebing.

Files:
MAIN_CircModel.py: Main entrypoint into model
set_initial_conditions.py: Generates parameters (e.g., ventricular, vessel resistances, etc) for the model
simulate_heart_beat.py: Simulates a cardiac cycle, calculates pressures and volumes in each compartment until the model reaches steady state
calculate_pressures.py: Calculates pressure in each compartment, using either P(t) = V(t)/C for vessels or P(t) = e(t) * (ESP(t) - EDP(t)) + EDP(t) for the ventricles
rk4.py: 4th order fixed step Runge-Kutta solver, determines volume change in each compartment
plotting_outputs.py: Plots PV loops, pressures and volumes vs time, flows vs time

