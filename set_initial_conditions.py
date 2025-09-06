"""
set_initial_conditions.py
Outputs initial volumes, timing, resistances, capacitances
"""
import numpy as np

def set_initial_conditions():

    # Heart parameters and SVR
    HR = 80 # heart rate (beats/min)
    BV = 250 # stressed blood volume (ml)
    LV_EES = 7 # LV end systolic elastance (mmHg/ml)
    LV_A = 0.1 # LV exponential constant in EDPVR (1/ml)
    RV_A = 0.09 # RV exponential constant in EDPVR (1/ml)
    B = 0.35 # LV linear constant in EDPVR (mmHg)
    V0 = 5 # unloaded LV volume (ml)
    SVR = 2.5 # systemic vascular resistance (mmHg*s/ml)

    # Initial volumes
    nRows = 5000
    Volumes = np.zeros((nRows, 6))
    Volumes[0, :] = BV / 6

    # Timing
    # Eq 3 from "Hemodynamic consequences of ventricular
    # interaction as assessed by model analysis" by Santamore and Burkhoff
    cycle_length = 60/HR # total length of one cardiac cycle (s)
    time_vector = np.linspace(0, cycle_length, nRows)
    tes = 0.2/0.75*cycle_length # Time to end systole (s)

    # Setting capacitances
    capacitances = np.zeros((4,))
    capacitances[0] = 3 # pulmonary venous compliance (ml/mmHg) Cvp
    capacitances[1] = 0.40 # systemic arterial compliance (ml/mmHg) Cas
    capacitances[2] = 17; # systemic venous compliance (ml/mmHg) Cvs
    capacitances[3] = 2 # pulmonary arterial compliance (ml/mmHg) Cap

    # Setting resistances
    resistances = np.zeros((7,))
    resistances[0] = 0.015 # pulmonary venous resistance (mmHg*s/ml) Rvp
    resistances[1] = 0.2 # characteristic resistance of aortic valve (mmHg*s/ml) Rcs
    resistances[2] = SVR # systemic arterial resistance (mmHg*s/ml) Ras
    resistances[3] = 0.015 # systemic venous resistance (mmHg*s/ml) Rvs
    resistances[4] = 0.06 # characteristic resistance of pulmonary valve (mmHg*s/ml) Rcp
    resistances[5] = 0.30 # pulmonary arterial resistance (mmHg*s/ml) Rap

    # Setting ventricular properties
    ventricles =  np.zeros((2,4)) # LV, then RV
    ventricles[0, 0] = LV_A
    ventricles[:, 1] = B
    ventricles[0, 2] = LV_EES
    ventricles[:, 3] = V0
    ventricles[1, 2] = LV_EES*(3/7)
    ventricles[1, 0] = RV_A

    return Volumes, time_vector, tes, ventricles, resistances, capacitances

