"""
calculate_pressures.py
Calculates pressures in each compartment throughout the cardiac cycle

Column  Compartment
0       pulmonary veins
1       left ventricle - surviving myocardium
2       systemic arteries
3       systemic veins
4       right ventricle
5       pulmonary arteries
6       optional, left ventricle infarct
"""
import math

def calculate_pressures(Volumes, Pressures, capacitances, ventricles, epsilon):

    # Calculate circulation pressures
    Pressures[0] = Volumes[0] / capacitances[0] # P_Cvp
    Pressures[2] = Volumes[2] / capacitances[1] # P_Cas
    Pressures[3] = Volumes[3] / capacitances[2] # P_Cvs
    Pressures[5] = Volumes[5] / capacitances[3] # P_Cap

    LV_params = ventricles[0, :] # A, B, Ees, V0
    RV_params = ventricles[1, :] # A, B, Ees*3/7, V0

    # Calculate RV Pressure
    RV_ESP = RV_params[2] * (Volumes[4] - RV_params[3])
    RV_EDP = RV_params[1] * (math.exp(RV_params[0] * (Volumes[4] - RV_params[3])) - 1)
    Pressures[4] = epsilon * (RV_ESP - RV_EDP) + RV_EDP

    # Calculate LV Pressure - Surviving myocardium
    LV_ESP = LV_params[2] * (Volumes[1] - LV_params[3])
    LV_EDP = LV_params[1] * (math.exp(LV_params[0] * (Volumes[1] - LV_params[3])) - 1)
    Pressures[1] = epsilon * (LV_ESP - LV_EDP) + LV_EDP

    return Pressures
