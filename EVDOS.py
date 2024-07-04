
"""
This file simulates the electric vehicle running status under the driving cycles.

@author: Shiqi Ou and Hao Jing
"""

import pandas as pd
from RunOnOrOff import EVDOS_RunTrips
from ModelPara import Initialize, ChargerType, VehicleInfo, BatAgeInfo, BatElecInputs, Lookup_OCVandR


def EVDOS():

    """
    This function aims to run the EVDOS model.
    """
    chargetype = "Level_1"
    BTMSOnOrOff = "On"
    HVACOnOrOff = "On"
    RBSOnOrOff = "On"
    
    
    yr_bgn = 1 #Simulation begin year
    years = 1 #Number of simulated years

    veh_df, charg_df = df_ini()

    chargtime, C_ini, mileage, Q_acc, runtime, TimStp_Age, TimStp_RunOff, TimStp_RunOn, T_acharg, T_b, T_c, usetime = Initialize()
    EnergyC = 0
    # Read customized inputs
    (chargpower, chargV, chargeff, chargprice) = ChargerType(chargetype)
    A_d, c_d, c_r, f_acc, f_pt, f_rbs, m_v, grav, rho_air, sigma, theta, v_wind = VehicleInfo()
    Lookup_SOC, Lookup_T, array_CalAgeT25, array_CalAgeT35, E_a, R_g, eta, zbar = BatAgeInfo()
    C_b, C_c, f_btms, K_ac, K_ab, K_bc, K_btms, P_d, Q_rad, T_low, T_up, V_max, V_min = BatElecInputs()
    SOC_OCVx, SOC_OCVy, SOC_Tba_Rx, SOC_Tba_Ry, SOC_Tba_Rz = Lookup_OCVandR()

    EVDOS_RunTrips(BTMSOnOrOff, chargetype, charg_df,HVACOnOrOff, RBSOnOrOff, years, yr_bgn, veh_df,chargtime, C_ini, mileage, Q_acc, runtime, TimStp_Age, TimStp_RunOff, TimStp_RunOn, T_acharg, T_b, T_c, usetime,chargpower, chargV, chargeff, chargprice,A_d, c_d, c_r, f_acc, f_pt, f_rbs, m_v, grav, rho_air, sigma, theta, v_wind,Lookup_SOC, Lookup_T, array_CalAgeT25, array_CalAgeT35, E_a, R_g, eta, zbar,C_b, C_c, f_btms, K_ac, K_ab, K_bc, K_btms, P_d, Q_rad, T_low, T_up, V_max, V_min,SOC_OCVx, SOC_OCVy, SOC_Tba_Rx, SOC_Tba_Ry, SOC_Tba_Rz)


def df_ini():
    
    C_ini = 198.5 #battery remaining capacity, unit: Ah.
    SOC_bgn = 0.8 #state of charge

    #Dataframe to save the updated vehicle and battery information on daily trips. 
    cols = ['Crate', 'D', 'VMT', 'Q_acc', 't_run', 'Day#', 'Year', 'EC']
    #Crate: battery remain capacity by the day end, unit: Ah.
    #D: cumulative battery using time (run+charg), unit: Day.
    #VMT: cumulative vehicle miles traveled, unit: Mile.
    #Q_acc: cumulated capacity output of battery throughout battery life so far, unit: kAh.
    #t_run: cumulative vehicle running time, unit: Hour.
    #Day#: day number.
    #Year: year number.
    #EC:energy consumption, unit: kwh.
    veh_df = pd.DataFrame(columns = cols)
    veh_df.loc[0] = [C_ini, 0, 0, 0, 0, 0, 1, 0] #[165.644457642651, 294.772569444445, 75914.4385013445, 113.179274234811, 2355.93194444444, 2019, 6]

    #Dataframe to store the updated charging information on daily trips. 
    cols = ['SOC_bgn', 'SOC_end', 'E_charg', 't_charg', 'c_charg', 'T_acharg',
            'D_charg', 'DayTripComplete']
    #SOC_bgn: battery state of charge at charging begin.
    #SOC_end: battery state of charge at charging end.
    #E_charg: charged energy, unit: kWh.
    #t_charg: charging time spent, unit: min.
    #c_charg: charging cost, unit: $.
    #T_acharg: temperature of ambient air when charging, unit: C.
    #D_charg: cummulative charging time, unit: mins.
    #DayTripComplete: complete the day trips or not, "Yes" or "No".
    charg_df = pd.DataFrame(columns = cols)
    charg_df.loc[0] = [SOC_bgn, SOC_bgn, 0, 0, 0, 0, 0, 'NA'] #[0.778765726823371, 0.800087095421187, 0.5975, 19.9166666666666, 0.077675, 11.65, 283116.583333333, '']

    return veh_df, charg_df
    
if __name__ == "__main__":
    EVDOS()
