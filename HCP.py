import sys
import math
import pandas
import numpy
import matplotlib.pyplot as plt

#pandas ref:    http://pandas.pydata.org/pandas-docs/version/0.20/whatsnew.html#whatsnew-0200-api-breaking
#Numpy ref:     https://docs.scipy.org/doc/numpy-1.12.0/reference/
#Matplotlib:    http://matplotlib.org/contents.html

#HCP Model Global Variables
C_i = 0.0         # CF for angl,                            Type:decimal 
c_conc = .25      # Cuttings conc=(%),                      Type:decimal 
c_mw = 8.834      # CF for mud density                      Type:decimal 
c_rpm = 0         # CF for rpm                              Type:int 
c_size = 0.0      # CF for rpm                              Type:int 

d_hole = 6.75     # Hole diameter                           Type:decimal
d_pipe = 5.00     # Drill pipe                              Type:decimal
rop = 100         # Rop                                     Type:decimal
rpm = 80          # Rpm                                     Type:int

f_fac = 0.00      # Friction factor                         Type:decimal

mud_pv  = 6       # Plastic viscosity                       Type:int 
mud_yp = 30        # Yield point                             Type:int 
u_a = 1           # Aparrent vis                            Type:int 

p_m = 10.05        # Density of mud                          Type:decimal 
p_f = 10.0        # Density of fluid                        Type:decimal 
p_s = 15.0        # Density of cuttings                     Type:decimal 

re = 1.00         # Reynolds number                         Type:decimal  

v_cut = 0.00      # Cutting velocity                        Type:decimal  
v_crit = 0.00     # Critical velocity                       Type:decimal  
v_min = 0.00      # Minimum velocity                        Type:decimal         
v_slip = 0.00     # Slip velocity                           Type:decimal  

inc = 0.00        # Inclination of well from vertical       Type:decimal  
d_cut = 0.5       # Diameter of cutting                     Type:decimal  


#Step 1 - Calculate v_CUT
def calc_V_Cut(ROP, d_PIPE, d_HOLE,c_CONC):
    V_CUT = rop / ( 
                    (36 * 
                        (1-
                            ( 
                                (d_pipe/d_hole)**2 
                            )
                        )
                    )*c_conc
                  )
    print("V_CUT:\t" + str(V_CUT))
    return V_CUT
#

#Step 2 - Calculate V_MIN
def calc_V_MIN(V_CUT,Vs1):
    V_MIN = V_CUT + Vs1

    print("V_MIN:\t" + str(V_MIN))
    return V_MIN    
#
  
#Step 3 - Calculate apparent viscosity
def calc_U_A(YP,PV,d_PIPE,d_HOLE, v_MIN):
    U_A = PV + (
                    (5*YP*
                        (d_HOLE-d_PIPE)
                    ) / v_MIN
               )
    print("U_A:\t" + str(U_A))
    return U_A

#
     
#Step 4 - Calculate Reynolds Number
def calc_RE(p_M, d_CUT, v_S1,u_A):
    RE = (
            (928 * p_M * d_CUT * v_S1)/u_A
         )

    print("RE:\t\t" + str(RE))
    return RE
#

#Step 4.1 - Calculate Friction FActor
def calc_F_FAC(RE):
    f_fac = 0.0
    if (RE < 3.0):
        f_fac = 40 / RE
    elif (RE > 3.0 and RE < 300.0):
        f_fac = 22/math.sqrt(RE)
    elif (RE > 300.0):
        f_fac = 1.54
    print("F_FAC:\t" + str(f_fac))
    return f_fac
#

#Step 5 - Calculate v_Slip
def calc_V_SLIP(f_FAC, d_CUT, p_S, p_M):
    V_SLIP = f_FAC * (  
                    d_CUT * 
                    (
                        math.sqrt(
                            (p_S-p_M)/p_M
                        )
                    )
                )

    print("V_SLIP:\t" + str(V_SLIP))
    return V_SLIP
#

#Step 6 - Bool

#Step 7 - 

#Step 8 - Calculate new v_min utilizing inc°
def calc_new_V_MIN(inc, v_CUT, v_SLIP, RPM, p_M):
    new_V_MIN = 0
    
    if (inc < 45):
        new_V_MIN  = (
            v_CUT + v_SLIP * (
                1  + (
                    inc* (
                        (600-RPM)*(3*p_M)/202500
                    )
                )
            )
        )
    elif(inc > 45):
        new_V_MIN  = (
            v_CUT + v_SLIP * (
                1  + (
                        (600-RPM)*(3*p_M)/4500
                )
            )
        )
    return new_V_MIN

#

#Input Parameters
def calc_HCM(p_s, p_f, d_hole, d_pipe, rop, mud_pv ,mud_yp, c_conc, p_m, d_cut):
    #Step 1
    V_CUT = calc_V_Cut(rop,d_pipe,d_hole,c_conc)

    #Asume Vs1 = 1 <- Can be 0 or 1
    Vs1 = 0.1
    print("Vs1:\t" + str(Vs1))

    #Step 2
    V_MIN = calc_V_MIN(V_CUT, Vs1)

    #TODO: figure out loop in model...?
   #while (math.abs(v_slip-Vs1) < 0.001): 
    
    #Step 3
    U_A = calc_U_A(mud_yp ,mud_yp, d_pipe, d_hole, V_MIN)

    #Step 4 <- p_M and d_Cut?????
    RE = calc_RE(p_m, d_cut, Vs1, U_A)

    #Step 4.1 - Calculate friction factor
    f_fac = calc_F_FAC(RE)
    
    #Step 5 - Calculaet v_Slip
    V_SLIP = calc_V_SLIP(f_fac, d_cut, p_s, p_m)



#Mud Calculation Variables
flow_In = 500

bit_size = 6.75
dp_size = 5.0

#

#Mud Calculations***************************************************************
    #Annular velocity in ft/s - Done
    #Annular_Velocity_ftpersec = ((24.5*flow_In)/((bit_size**2)-(dp_size**2))/60)
    #print("Annular Velocity:\t" + str(Annular_Velocity_ftpersec))

    #n_Annulus
    #calculates the n value (Power Law Index) of drilling fluid in annulus using 100 and 3 RPM rheology readings (dimensionless)
    #n_Annulus = (0.657*log10(Vis_100_RPM/Vis_3_RPM))
    #,
    
    #K_Annulus
    #calculates the K value (Consistency Index) of drilling fluid in annulus using 100 RPM rheology reading and the previously calculated n Annulus value (dimensionless)
    #     ***NOTES***
    #     Derived from n & K sep 2005 paper found here: X:\Drilling Engineering\Engineering\Drilling Technology\Steve Scarver\ETG\Hole Cleaning\Other Papers\n & K sep 2005.pdf
    #K_Annulus = (5.11*(Vis_100_RPM/(170.2^n_Annulus)))
    #,
    
    #mu_Annulus
    #calculates the effective viscosity of drilling fluid in the annulus using n and K values, Annular Velocity, Hole diameter, pipe OD (in centipoise)
    #mu_Annulus = (100*K_Annulus*((144*Annular_Velocity_ftpersec/(Bit_Size-DP_size))^(n_Annulus-1))*((((2*n_Annulus)+1)/(3*n_Annulus))^n_Annulus))
    #,
    
    #Re_Annulus (Reynold's Number)
    #calculates the Reynolds number of drilling fluid in the annulus using Hole Diameter, Pipe OD, Annular Velocity, Mud Weight, and the mu viscosity
    #Re_Annulus = ((928*(Bit_Size-DP_size)*Annular_Velocity_ftpersec*MW)/mu_Annulus)
    #,
    
    #f Annulus
    #calculates the f value in the Annulus based on Reynolds number
    #f_Annulus = 24/Re_Annulus
    #,
    
    #Cuttings Concentration
    #calculates the instantaneous accumulation of cuttings based on ROP (injection rate)
    #Cuttings_Concentration = ((0.01778*(Footage_Made*720))+1.505)
    #,
    
    #Cuttings Diameter
    #calculates the size of cuttings being generated based on ROP (injection rate) and grinding effect of RPM
    #Cuttings_Diameter = (Footage_Made*720)/(60*RPM)
    #,
    
    #Mud Weight Correction factor
    #applies a correction to slip velocity based on Mud Weight
    #C_MW = ((3+MW)/15)
    #,
    
    #RPM Correction factor
    #applies a correction to slip velocity based on RPM of drillpipe
    #C_RPM = ((600-RPM)/600)
    #,
    
    #Inclination Correction factor applies a correction to slip velocity based on degrees inclination of the hole
    #C_inc = ifelse(Inc > 45.0,(1+((2*Inc)/45)),2)
    #,
    
    #Slip velocity
    #calculates the rate at which cuttings will slip in drilling fluid based on viscosity, mud weight, and cuttings size
    #V_slip = f_Annulus*sqrt(Cuttings_Diameter*((Cuttings_Density-MW)/MW))
    #,
    
    #Cuttings transport velocity
    #calculates the velocity of cuttings based on volumetric injection rate, hole diameter, and pipe OD
    #V_cut = (((Footage_Made*720)/(36*(1-(DP_size/Bit_Size)^2)*Cuttings_Concentration)))
    #,
    
    #Minimum transport velocity 
    #calculates the annular velocity needed to transport cuttings out of the hole based on slip velocity, cuttings velocity,
    #     and all correction factors applied to slip velocity (RPM, Inclination, and mud weight)
    #V_min = (V_cut+((1+C_Inc*C_MW*C_RPM)*V_slip))
    #,
    
    #Percent efficiency (hole ceaning velocities comparison)
    #Compares annular velocity to minimum transport velocity
    #Efficiency = ifelse(Annular_Velocity_ftpersec/V_min>1,1,Annular_Velocity_ftpersec/V_min)

#

#Run HCM with initial parameters - for testing
calc_HCM(p_s, p_f, d_hole, d_pipe, rop, mud_pv ,mud_yp, c_conc, p_m, d_cut)

#Main Function
    #1 - Func -> get well info()
        #a - Header Info (District, PN, etc.)
        #b - Wellbore set md's
        #c - Casing set md's
        #d - Drill pipe info
        #e - Mud Properties
        #f - Bit info
        #g - Survey Information
        #Note: info will have to be the most recent data from WV & CHKShot

    #2 - Func -> get TimeLog Data()
      
    #3 - Func -> Calculations
        #a - Mud Calcs
        #b - Hole Cleaning Calcs
        #c - Build func to loop table to get  values 
        #d - Build Func to loop tables to set values
        #e - Build Func to add Column(s) to (virtual)Table
        #e - Build Func to remove Column(s) to (virtual)Table
        #f - Calculate drilling status

    #4 - Func -> Build to accomidate for Real-Time and Historic data sets
        #a - Build manual get info 
        #b - Build refreshing query to auto get info  