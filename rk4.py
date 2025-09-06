"""
rk4.py
4th order Runge-Kutta method to calculate change in volume in each compartment

Column  Compartment
0       pulmonary veins
1       left ventricle - surviving myocardium
2       systemic arteries
3       systemic veins
4       right ventricle
5       pulmonary arteries
6       optional, left ventricle infarct
"""
import numpy as np
import math
from DogPVSimulation_6Comp_Python.calculate_pressures import calculate_pressures

def rk4(current_volumes, current_pressures, resistances, capacitances, ventricles,
        step_size, current_time, tes):

    # compartment functions
    def dv1(P_pa, P_pv, P_lv, R_pa, R_pv, R_mv):
        """Pulmonary veins"""
        Q_in = (P_pa - P_pv) / R_pa
        Q_out = (P_pv - P_lv) / R_pv * (P_pv > P_lv) - (P_pv - P_lv) / R_mv * (P_lv > P_pv)
        delta_vol = Q_in - Q_out
        return delta_vol

    def dv2(P_pv, P_lv, P_sa, R_pv, R_cs, R_mv):
        """Non-infarcted LV"""
        Q_in = (P_pv - P_lv) / R_pv * (P_pv > P_lv) + (P_pv - P_lv) / R_mv * (P_lv > P_pv)
        Q_out = (P_lv - P_sa) / R_cs * (P_lv > P_sa)
        delta_vol = Q_in - Q_out
        return delta_vol

    def dv3(P_lv, P_sa, P_sv, R_cs, R_sa):
        """Systemic arteries"""
        Q_in = (P_lv - P_sa) / R_cs * (P_lv > P_sa)
        Q_out = (P_sa - P_sv) / R_sa
        delta_vol = Q_in - Q_out
        return delta_vol

    def dv4(P_sa, P_sv, P_rv, R_sa, R_sv):
        """Systemic veins"""
        Q_in = (P_sa - P_sv) / R_sa
        Q_out = (P_sv - P_rv) / R_sv * (P_sv > P_rv)
        delta_vol = Q_in - Q_out
        return delta_vol

    def dv5(P_sv, P_rv, P_pa, R_sv, R_cp):
        """Right ventricle"""
        Q_in = (P_sv - P_rv) / R_sv * (P_sv > P_rv)
        Q_out = (P_rv - P_pa) / R_cp * (P_rv > P_pa)
        delta_vol = Q_in - Q_out
        return delta_vol

    def dv6(P_rv, P_pa, P_pv, R_cp, R_pa):
        """Pulmonary arteries"""
        Q_in = (P_rv - P_pa) / R_cp * (P_rv > P_pa)
        Q_out = (P_pa - P_pv) / R_pa
        delta_vol = Q_in - Q_out
        return delta_vol


    # initialize
    half_step = step_size / 2
    sixth_step = step_size / 6
    new_vols = np.zeros((6,))
    new_pres = np.zeros((6,))
    resistances[6] = math.inf

    # find current contraction timepoint
    if current_time < 2 * tes:
        epsilon = (1/2) * (1 - math.cos(math.pi * current_time / tes))
    else:
        epsilon = 0

    # k1
    k1 = np.array([dv1(current_pressures[5], current_pressures[0], current_pressures[1], resistances[5], resistances[0], resistances[6] ),
          dv2(current_pressures[0], current_pressures[1], current_pressures[2], resistances[0], resistances[1], resistances[6] ),
          dv3(current_pressures[1], current_pressures[2], current_pressures[3], resistances[1], resistances[2] ),
          dv4(current_pressures[2], current_pressures[3], current_pressures[4], resistances[2], resistances[3] ),
          dv5(current_pressures[3], current_pressures[4], current_pressures[5], resistances[3], resistances[4] ),
          dv6(current_pressures[4], current_pressures[5], current_pressures[0], resistances[4], resistances[5] )])

    # k2
    P_k2 = current_pressures + half_step * k1
    k2 = np.array([dv1(P_k2[5], P_k2[0], P_k2[1], resistances[5], resistances[0], resistances[6]),
          dv2(P_k2[0], P_k2[1], P_k2[2], resistances[0], resistances[1], resistances[6]),
          dv3(P_k2[1], P_k2[2], P_k2[3], resistances[1], resistances[2]),
          dv4(P_k2[2], P_k2[3], P_k2[4], resistances[2], resistances[3]),
          dv5(P_k2[3], P_k2[4], P_k2[5], resistances[3], resistances[4]),
          dv6(P_k2[4], P_k2[5], P_k2[0], resistances[4], resistances[5])])

    # k3
    P_k3 = current_pressures + half_step * k2
    k3 = np.array([dv1(P_k3[5], P_k3[0], P_k3[1], resistances[5], resistances[0], resistances[6]),
          dv2(P_k3[0], P_k3[1], P_k3[2], resistances[0], resistances[1], resistances[6]),
          dv3(P_k3[1], P_k3[2], P_k3[3], resistances[1], resistances[2]),
          dv4(P_k3[2], P_k3[3], P_k3[4], resistances[2], resistances[3]),
          dv5(P_k3[3], P_k3[4], P_k3[5], resistances[3], resistances[4]),
          dv6(P_k3[4], P_k3[5], P_k3[0], resistances[4], resistances[5])])

    # k4
    P_k4 = current_pressures + step_size * k3
    k4 = np.array([dv1(P_k4[5], P_k4[0], P_k4[1], resistances[5], resistances[0], resistances[6]),
          dv2(P_k4[0], P_k4[1], P_k4[2], resistances[0], resistances[1], resistances[6]),
          dv3(P_k4[1], P_k4[2], P_k4[3], resistances[1], resistances[2]),
          dv4(P_k4[2], P_k4[3], P_k4[4], resistances[2], resistances[3]),
          dv5(P_k4[3], P_k4[4], P_k4[5], resistances[3], resistances[4]),
          dv6(P_k4[4], P_k4[5], P_k4[0], resistances[4], resistances[5])])

    new_vols = current_volumes + sixth_step * (k1 + 2 * k2 + 2 * k3 + k4)
    new_pres = calculate_pressures(new_vols, new_pres, capacitances, ventricles, epsilon)
    return new_vols, new_pres