# -*- coding: utf-8 -*-
"""
This file aims to include all parameters used in EVDOS model

@author: Shiqi Ou
"""

import numpy as np

def Initialize():
    
    C_ini = 198.5 #battery remaining capacity, unit: Ah.
    T_acharg = 25. #temperature of ambient air (charging), unit: C.
    T_b = 25. #temperature of battery, unit: C.
    T_c = 25. #temperature of vehicle cabin, unit: C.
    TimStp_RunOn = 1. #time step for vehicle stop/charging, unit: sec.
    TimStp_RunOff = 5. #time step for vehicle running, unit: sec.
    TimStp_Age = 60. #time step for calculating battery aging, unit: sec.

    usetime = 0. #cumulative battery using time (run + charging), unit: days.
    mileage = 0. #cumulative vehicle miles traveled, unit: miles.
    Q_acc = 0. #cumulative capacity output of battery, unit: kAh.
    runtime = 0. #cumulative vehicle running time, unit: hrs.
    EnergyC=0. #daily energy consumption, unit: kwh.

    chargtime = 0. #cumulative battery charged time so far, unit: mins.

    return chargtime, C_ini, mileage, Q_acc, runtime, TimStp_Age, TimStp_RunOff, TimStp_RunOn, T_acharg, T_b, T_c, usetime


def ChargerType(ChargeType):
    #Charger inforamtion input:
    #Charging power, unit: kW.
    #Charging voltage, unit: V.
    #Charging efficient.
    #Charging price, unit: $/kWh.
    ChargeInfo = {"Level_1": (1.8, 120., 0.85, 0.13), 
                  "Level_2": (7.6, 240., 0.85, 0.13),
                  "DC_Fast": (60, 480., 0.85, 0.26), 
                  "Extreme_Fast": (400, 800., 0.85, 0.52)}
    return ChargeInfo[ChargeType]


def VehicleInfo():
    """
    Vehicle kinetics information input
    """
    rho_air = 1.225 #air density, unit: kg/m^3
    A_d = 2.130 #front area, unit: m^2
    c_d = 0.350 #coefficient of aerodynamic resistance
    c_r = 0.015 #rolling resistance coefficient
    m_v = 1100. #vehicle gross weight, unit: kg
    grav = 9.810 #gravitational constant, unit: m/s^2
    theta = 0. #road inclination, unit: deg
    v_wind = 0. #wind speed, unit: m/s
    sigma = 1.3 #correction coefficient of rotational inertia

    """
    Powertrain information:
    
    Power to HVAC system:
    COP = 1.5 for cooling, and COP = 2.5 for heating.
    Reference: https://www.energy.gov/sites/prod/files/2014/03/f8/deer12_maranville.pdf
    COP = ratio heat dissipation/electrical power intake
    """
    f_pt = 0.9 #powertrain efficiency (energy from bat to wheel)
    f_acc = 0.98 #accessory efficiency (electronics etc)
    
    """
    f_rbs is an average value which estimates the ratio of stored electricity 
    energy over braking energy; and this value is also correlated to vehicle 
    speed, deceleration, ambient temperature.

    Now it is assumed to be 0.63 (https://doi.org/10.1016/j.apenergy.2016.01.051).
    Boretti 2013 believes it ranges from 31% to 79% and it is related to temperature.
    (https://doi.org/10.4271/2013-01-2872)
    Reference source: https://www.sciencedirect.com/topics/engineering/regenerative-brakingIf
    """
    f_rbs = 0.63 #0.63 regenarative efficiency (stored energy/braking energy)
    
    return A_d, c_d, c_r, f_acc, f_pt, f_rbs, m_v, grav, rho_air, sigma, theta, v_wind


def BatAgeInfo():
    """
    Lookup table for calendar degradation (% of battery initial capacity)
    The calender degradation is based on reference: https://doi.org/10.3390/app8101825
    Eq. (5) (SOC=0.15) and (6) (SOC=0.9).
    """
    Lookup_SOC = [0., 0.15, 0.9, 1.00]
    Lookup_T = [0, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 
            2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000, 
            4200, 4400, 4600, 4800, 5000, 5200, 5400, 5600, 5800, 6000, 
            6200, 6400, 6600, 6800, 7000, 7200, 7400, 7600, 7800, 8000]
    array_CalAgeT25 = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                              1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0.99378297, 0.989654419, 0.985847604, 0.982100597, 0.978374526, 
     0.974663584, 0.970966865, 0.967284189, 0.963615483, 0.959960693, 
     0.956319764, 0.952692645, 0.949079283, 0.945479625, 0.94189362, 
     0.938321216, 0.934762362, 0.931217005, 0.927685096, 0.924166582, 
     0.920661413, 0.917169538, 0.913690907, 0.91022547, 0.906773177, 
     0.903333978, 0.899907822, 0.896494662, 0.893094447, 0.889707128, 
     0.886332656, 0.882970983, 0.879622061, 0.87628584, 0.872962272, 
     0.86965131, 0.866352906, 0.863067012, 0.859793581, 0.856532565], 
    [0.993961538, 0.970790021, 0.958914071, 0.947185985, 0.935601341, 0.924158383,
     0.91285538, 0.90169062, 0.890662411, 0.879769083, 0.869008987, 0.858380494, 
     0.847881994, 0.837511896, 0.82726863, 0.817150646, 0.807156411, 0.797284411, 
     0.787533152, 0.777901156, 0.768386965, 0.758989139, 0.749706253, 0.740536903, 
     0.731479699, 0.72253327, 0.713696261, 0.704967334, 0.696345167, 0.687828455, 
     0.679415906, 0.671106248, 0.662898222, 0.654790585, 0.64678211, 0.638871582, 
     0.631057805, 0.623339596, 0.615715784, 0.608185216, 0.600746752],
     [0.99315641, 0.967724294, 0.954815358, 0.942031102, 0.92940144, 0.916929564, 
      0.904614286, 0.892453787, 0.880446174, 0.868589563, 0.856882093, 0.845321925, 
      0.83390724, 0.822636244, 0.811507165, 0.80051825, 0.78966777, 0.778954018, 
      0.768375305, 0.757929964, 0.74761635, 0.737432836, 0.727377815, 0.717449702, 
      0.70764693, 0.697967949, 0.688411232, 0.678975269, 0.669658568, 0.660459656, 
      0.651377077, 0.642409394, 0.633555188, 0.624813055, 0.616181612, 0.60765949, 
      0.599245338, 0.590937821, 0.58273562, 0.574637434, 0.566641977]])

    array_CalAgeT35 = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0.990384615, 0.984615385, 0.980769231, 0.9789, 0.9749, 0.9709, 0.9669,
     0.9629, 0.9589, 0.9549, 0.9509, 0.9469, 0.9429, 0.9389, 0.9349, 0.9309,
     0.9269, 0.9229, 0.9189, 0.9149, 0.9109, 0.9069, 0.9029, 0.8989, 0.8949,
     0.8909, 0.8869, 0.8829, 0.8789, 0.8749, 0.8709, 0.8669, 0.8629, 0.8589,
     0.8549, 0.8509, 0.8469, 0.8429, 0.8389, 0.8349],
    [0.990384615, 0.958846154, 0.953846154, 0.914615385, 0.9067, 0.8867, 0.8667,
     0.8467, 0.8267, 0.8067, 0.7867, 0.7667, 0.7467, 0.7267, 0.7067, 0.6867, 
     0.6667, 0.6467, 0.6267, 0.6067, 0.5867, 0.5667, 0.5467, 0.5267, 0.5067,
     0.4867, 0.4667, 0.4467, 0.4267, 0.4067, 0.3867, 0.3667, 0.3467, 0.3267,
     0.3067, 0.2867, 0.2667, 0.2467, 0.2267, 0.2067, 0.1867],
    [0.989402399, 0.955133375, 0.949162231, 0.907727409, 0.899164015, 0.87760625,
     0.856047018, 0.834486916, 0.812926256, 0.791365217, 0.76980391, 0.748242404,
     0.72668075, 0.705118979, 0.683557117, 0.661995182, 0.640433186, 0.61887114,
     0.597309053, 0.575746931, 0.554184778, 0.5326226, 0.5110604, 0.489498181,
     0.467935944, 0.446373692, 0.424811428, 0.403249151, 0.381686864, 0.360124567,
     0.338562262, 0.316999949, 0.295437629, 0.273875302, 0.25231297, 0.230750633,
     0.20918829, 0.187625944, 0.166063593, 0.144501238, 0.122938879]])


    """
    Battery aging degradation information input:
    
    Reference: Suri et al. 2016. https://doi.org/10.1016/j.energy.2015.11.075
    Description: The aging model was not validated across different temperatures,
             and capacity loss dependence on temperature was modeled using
             an Arrhenius-like equation. (Using the Arrhenius-like equation to
             fit the experimental data, so it is an emperical equation.)

    Following are the parameters for calculating battery thermal degradation 
    (% of battery initial capacity).
    """
    E_a = 31500 #activation energy, unit: J/mol
    R_g = 8.314 #universal gas constant, unit: J/mol-K
    eta = 152.6 #battery current dependence
    zbar = 0.4 #coefficient

    return Lookup_SOC, Lookup_T, array_CalAgeT25, array_CalAgeT35, E_a, R_g, eta, zbar


def BatElecInputs():
    """
    Battery genernal information:
    """
    V_max = 400. #max voltage, unit: V
    V_min = 270. #min voltage, unit: V
    P_d = 85. #max deliverable energy, unit: kWh

    """
    Battery thermal basic information:
    """
    C_b = 101771. #heat capacity of battery, unit: J/K
    C_c = 182000. #heat capacity of vehicle cabin, unit: J/K
    K_ac = 22.6 #effective heat transfer coefficient between ambient & cabin, unit: W/K
    K_ab = 4.343 #effective heat transfer coefficient between ambient & battery, unit: W/K
    K_bc = 3.468 #effective heat transfer coefficient between battery & cabin, unit: W/K
    Q_rad = 0. #solar irradiance (default = 0), unit: kW

    """
    Battery thermal management system information:
    """
    T_up = 30. #temperature ceiling boundary that the BTMS is not working, unit: C
    T_low = 10. #temperature bottom boundary that the BTMS is not working, unit: C
    K_btms = 340. #effective heat transfer between battery and battery thermal management system, unit: W/K 
    f_btms = 0. #coefficient of BTMS performance (ratio between BTMS heat transfer and BTMS power)
    
    return C_b, C_c, f_btms, K_ac, K_ab, K_bc, K_btms, P_d, Q_rad, T_low, T_up, V_max, V_min


def Lookup_OCVandR():
    """
    Lookup table for OCV vs SOC (% of battery initial capacity)
    """
    SOC_OCVx = [0., 0.2, 0.5, 0.9, 1.0]
    SOC_OCVy = [333., 351., 364., 388., 400.]

    """
    Lookup table for internal resistance of the whole battery pack (R vs SOC & T_ba)
    """
    SOC_Tba_Rx = np.arange(0., 1.1, 0.1)
    SOC_Tba_Ry = [-15., 0., 30.]
    SOC_Tba_Rz = np.array([[1.340, 1.080, 0.320],
                  [1.340, 1.080, 0.200],
                  [1.340, 1.080, 0.150],
                  [1.340, 0.300, 0.125],
                  [0.680, 0.250, 0.125],
                  [0.485, 0.260, 0.130],
                  [0.430, 0.250, 0.130],
                  [0.415, 0.240, 0.160],
                  [0.420, 0.255, 0.165],
                  [0.430, 0.260, 0.130],
                  [0.440, 0.270, 0.130]])
    
    return SOC_OCVx, SOC_OCVy, SOC_Tba_Rx, SOC_Tba_Ry, SOC_Tba_Rz