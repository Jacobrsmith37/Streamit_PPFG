#!pip install streamlit
#Import the required Libraries
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import lasio



# read the las file and show the headers, or 'keys'
las = lasio.read("OVBD_PSI.las")
# store the las file in df variable as a pandas dataframe
df_ovbd = las.df()
df_ovbd.isna().sum()
# reindex
df_ovbd = df_ovbd.rename_axis('DEPTH').reset_index()

# ***LOG MD SHIFT***
shift = 32

def main():
    if len(df_ovbd) == 0:
        print(f'Warning! The log is empty.')
        return

    else:
        df_ovbd['DEPTH'] = df_ovbd['DEPTH'] + shift
    
    
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)


# *** CREATE COPY OF OVBD_PPG_MD_SHIFTED TO MAKE LOW SIDE PORE PRESSURE LOG AND EDIT ***
# WILL CONVERT TO PPG LATER

df_LS = df_ovbd.copy()
df_LS.rename(columns={'OVBD_PSI': 'LS_PSI'}, inplace=True)  
df_ML = df_ovbd.copy()
df_ML.rename(columns={'OVBD_PSI': 'ML_PSI'}, inplace=True)
df_HS = df_ovbd.copy()
df_HS.rename(columns={'OVBD_PSI': 'HS_PSI'}, inplace=True)

# END COPY KB SHIFTED OVBD LOG


# Bring in topset and remove last column
Topset1 = pd.read_csv(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\Updated_PPFG\Topset1_Updated_PPFG.txt', sep = "\t")
Topset1.drop('GeosteeringDip', axis = 1, inplace = True)

Topset1['TopName'] = Topset1['TopName'].str.title()
    
        
        
        
# Standard Variables
Water_Table_Elev = 100.0
Seabed_Elev = 200.0
Base_Zone_1 = 14000
Base_Zone_2 = 14000
Base_Zone_3 = 15000
Base_Zone_4 = 16000
Base_Zone_5 = 17000

# Variables for Low Side Pore Pressure
LS_Sea_Water_Density = 0.45
LS_Formation_water_Density_1 = 0.45
LS_Formation_water_Density_2 = 0.52
LS_Formation_water_Density_3 = 0.45
LS_Formation_water_Density_4 = 0.45
LS_Formation_water_Density_5 = 0.45

# Variables for Most Likely Pore Pressure
ML_Sea_Water_Density = 0.47
ML_Formation_water_Density_1 = 0.47
ML_Formation_water_Density_2 = 0.52
ML_Formation_water_Density_3 = 0.47
ML_Formation_water_Density_4 = 0.47
ML_Formation_water_Density_5 = 0.47

# Variables for High Side Pore Pressure
HS_Sea_Water_Density = 0.49
HS_Formation_water_Density_1 = 0.49
HS_Formation_water_Density_2 = 0.52
HS_Formation_water_Density_3 = 0.49
HS_Formation_water_Density_4 = 0.49
HS_Formation_water_Density_5 = 0.49

# Variables for Low Side known pressure anomoly zones
LS_inyan_kara = 3200
LS_20_high_amsden = None
LS_300_low_rival = None
LS_upper_bakken = 8400

# Variables for Most Likely known pressure anomoly zones
ML_inyan_kara = 3600
ML_swift = None
ML_20_high_amsden = None
ML_300_low_rival = None
ML_upper_bakken = 8850

# Variables for High Side known pressure anomoly zones
HS_inyan_kara = 3700
HS_swift = None
HS_20_high_amsden = None
HS_300_low_rival = None
HS_upper_bakken = 9200

greenhorn = Topset1[Topset1['TopName'] == 'Greenhorn']
belle_fourche = Topset1[Topset1['TopName'] == 'Belle_Fourche']
mowry = Topset1[Topset1['TopName'] == 'Mowry']
inyan_kara = Topset1[Topset1['TopName'] == 'Inyan_Kara']
swift = Topset1[Topset1['TopName'] == 'Swift']
rierdon = Topset1[Topset1['TopName'] == 'Rierdon']
amsden = Topset1[Topset1['TopName'] == 'Amsden']
tyler = Topset1[Topset1['TopName'] == 'Tyler']
kibbey_lime = Topset1[Topset1['TopName'] == 'Kibbey_Lime']
charles = Topset1[Topset1['TopName'] == 'Charles']
top_last_salt = Topset1[Topset1['TopName'] == 'Top_Last_Salt']
base_last_salt = Topset1[Topset1['TopName'] == 'Base_Last_Salt']
frobisher_alida = Topset1[Topset1['TopName'] == 'Frobisher-Alida_Interval']
lodgepole = Topset1[Topset1['TopName'] == 'Lodgepole']
upper_bakken = Topset1[Topset1['TopName'] == 'Upper_Bakken']
middle_bakken = Topset1[Topset1['TopName'] == 'Middle_Bakken']
lower_bakken = Topset1[Topset1['TopName'] == 'Lower_Bakken']
three_forks = Topset1[Topset1['TopName'] == 'Three_Forks']
birdbear = Topset1[Topset1['TopName'] == 'Birdbear']       
        
        
        # initialize list of lists
data = [
    ['shale', 0.724, 0.0], 
    ['sand', 0.500, 0.0],
    ['limestone', 0.449, 150],
    ['dolomite', 0.389, 400],
    ['anhydrite', 0.471, 600],
    ['dolomitic limestone', 0.429, 200],
    ['siltstone', 0.500, 200],
    ['coal', 0.800, 0.0]
]
# Create the pandas DataFrame
df_lith = pd.DataFrame(data, columns = ['Lith', 'Kf', 'Ts'])
        
################ LOW SIDE #######################     
                
def LS_calcs():
    for i in range(len(df_LS)):
        if df_LS['DEPTH'][i] <= Water_Table_Elev + shift:
            df_LS['LS_PSI'][i] = 0
            
        elif df_LS['DEPTH'][i] <= Seabed_Elev + shift:
            df_LS['LS_PSI'][i] = (df_LS['DEPTH'][i] - Water_Table_Elev - shift) * LS_Sea_Water_Density
            
        elif df_LS['DEPTH'][i] <= Base_Zone_1 + shift:
             df_LS['LS_PSI'][i] = (LS_Formation_water_Density_1) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PSI'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_2 + shift:
             df_LS['LS_PSI'][i] = (LS_Formation_water_Density_2) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PSI'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_3 + shift:
             df_LS['LS_PSI'][i] = (LS_Formation_water_Density_3) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PSI'][i-1]
                
        elif df_LS['DEPTH'][i] <= Base_Zone_4 + shift:
             df_LS['LS_PSI'][i] = (LS_Formation_water_Density_4) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PSI'][i-1]
                
        else:
             df_LS['LS_PSI'][i] = (LS_Formation_water_Density_5) * (df_LS['DEPTH'][i] - df_LS['DEPTH'][i-1]) +  df_LS['LS_PSI'][i-1]              

                
    for i in range(len(df_LS)):
    
        if LS_inyan_kara == None:
            continue
        if df_LS['DEPTH'][i] in range(
              (int(inyan_kara.MD)),
              (int(inyan_kara.MD) + 20)):
                 df_LS['LS_PSI'][i] = LS_inyan_kara
            
    for i in range(len(df_LS)):                
        if LS_inyan_kara == None:
            continue
        if df_LS['DEPTH'][i] in range(
             (int(inyan_kara.MD) + 20),
             (int(swift.MD))):
                df_LS['LS_PSI'][i] =  (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1])  
                

    for i in range(len(df_LS)):
        if LS_20_high_amsden == None:
            continue
        if df_LS['DEPTH'][i] in range(
             (int(amsden.MD) - 20),
             (int(amsden.MD) + 0)):
                 df_LS['LS_PSI'][i] = LS_20_high_amsden

    for i in range(len(df_LS)):            
        if LS_300_low_rival == None:
            continue
        if round(df_LS['DEPTH'][i]) in range(
            (int(frobisher_alida.MD) - 10),
            (int(frobisher_alida.MD) + 10)):
                 df_LS['LS_PSI'][i] = LS_300_low_rival
            
            
            
    for i in range(len(df_LS)):     
        if LS_300_low_rival == None:
            continue
        if round(df_LS['DEPTH'][i]) in range(
            (int(frobisher_alida.MD) + 10),
            (int(frobisher_alida.MD) + 130)):
                df_LS['LS_PSI'][i] = (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1]) 
            
    for i in range(len(df_LS)):            
        if LS_upper_bakken == None:
            continue
        if round(df_LS['DEPTH'][i]) in range(
            (int(upper_bakken.MD) + 0),
            (int(upper_bakken.MD) + 160)):
            df_LS['LS_PSI'][i] = LS_upper_bakken
                        
        
        
################ MOST LIKELY #######################     
        
def ML_calcs():
    for i in range(len(df_ML)):
        if df_ML['DEPTH'][i] <= Water_Table_Elev + shift:
            df_ML['ML_PSI'][i] = 0
            
        elif df_ML['DEPTH'][i] <= Seabed_Elev + shift:
            df_ML['ML_PSI'][i] = (df_ML['DEPTH'][i] - Water_Table_Elev - shift) * ML_Sea_Water_Density
            
        elif df_ML['DEPTH'][i] <= Base_Zone_1 + shift:
             df_ML['ML_PSI'][i] = (ML_Formation_water_Density_1) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PSI'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_2 + shift:
             df_ML['ML_PSI'][i] = (ML_Formation_water_Density_2) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PSI'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_3 + shift:
             df_ML['ML_PSI'][i] = (ML_Formation_water_Density_3) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PSI'][i-1]
                
        elif df_ML['DEPTH'][i] <= Base_Zone_4 + shift:
             df_ML['ML_PSI'][i] = (ML_Formation_water_Density_4) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PSI'][i-1]
                
        else:
             df_ML['ML_PSI'][i] = (ML_Formation_water_Density_5) * (df_ML['DEPTH'][i] - df_ML['DEPTH'][i-1]) +  df_ML['ML_PSI'][i-1]
                

    for i in range(len(df_ML)): 
        if ML_inyan_kara == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(inyan_kara.MD)),
             (int(inyan_kara.MD) + 20)):
                df_ML['ML_PSI'][i] = ML_inyan_kara
                
    for i in range(len(df_ML)):                 
        if ML_inyan_kara == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(inyan_kara.MD) + 20),
             (int(swift.MD))):
                df_ML['ML_PSI'][i] =  (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])     
                
    for i in range(len(df_ML)):                 
        if ML_20_high_amsden == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(amsden.MD) - 20),
             (int(amsden.MD) + 0)):
                df_ML['ML_PSI'][i] = ML_20_high_amsden 
                
    for i in range(len(df_ML)):                 
        if ML_300_low_rival == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(frobisher_alida.MD) - 10),
             (int(frobisher_alida.MD + 10))):
                df_ML['ML_PSI'][i] = ML_300_low_rival
                
    for i in range(len(df_ML)):                 
        if ML_300_low_rival == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(frobisher_alida.MD) + 10),
             (int(frobisher_alida.MD + 130))):
                df_ML['ML_PSI'][i] = (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])   
                
    for i in range(len(df_ML)):                 
        if ML_upper_bakken == None:
            continue
        if df_ML['DEPTH'][i] in range(
             (int(upper_bakken.MD)),
             (int(upper_bakken.MD) + 160)):
                df_ML['ML_PSI'][i] = ML_upper_bakken     
                        
        
        
################ HIGH SIDE #######################    

def HS_calcs():
    for i in range(len(df_HS)):
        if df_HS['DEPTH'][i] <= Water_Table_Elev + shift:
            df_HS['HS_PSI'][i] = 0
            
        elif df_HS['DEPTH'][i] <= Seabed_Elev + shift:
            df_HS['HS_PSI'][i] = (df_HS['DEPTH'][i] - Water_Table_Elev - shift) * HS_Sea_Water_Density
            
        elif df_HS['DEPTH'][i] <= Base_Zone_1 + shift:
             df_HS['HS_PSI'][i] = (HS_Formation_water_Density_1) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PSI'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_2 + shift:
             df_HS['HS_PSI'][i] = (HS_Formation_water_Density_2) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PSI'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_3 + shift:
             df_HS['HS_PSI'][i] = (HS_Formation_water_Density_3) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PSI'][i-1]
                
        elif df_HS['DEPTH'][i] <= Base_Zone_4 + shift:
             df_HS['HS_PSI'][i] = (HS_Formation_water_Density_4) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PSI'][i-1]
                
        else:
             df_HS['HS_PSI'][i] = (HS_Formation_water_Density_5) * (df_HS['DEPTH'][i] - df_HS['DEPTH'][i-1]) +  df_HS['HS_PSI'][i-1]
                
                
                
                
    for i in range(len(df_HS)): 
        if HS_inyan_kara == None:
            continue
        if df_HS['DEPTH'][i] in range(
             (int(inyan_kara.MD)),
             (int(inyan_kara.MD) + 20)):
                df_HS['HS_PSI'][i] = HS_inyan_kara
            
    for i in range(len(df_HS)):                 
        if HS_inyan_kara == None:
                continue
        if df_HS['DEPTH'][i] in range(
             (int(inyan_kara.MD) + 20),
             (int(swift.MD))):
                df_HS['HS_PSI'][i] =  (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])
            
    for i in range(len(df_HS)):                 
        if HS_20_high_amsden == None:
            continue
        if df_HS['DEPTH'][i] in range(
             (int(amsden.MD) - 20),
             (int(amsden.MD) + 0)):
                df_HS['HS_PSI'][i] = HS_20_high_amsden 
            
    for i in range(len(df_HS)):                 
        if HS_300_low_rival == None:
            continue
        if df_HS['DEPTH'][i] in range(
             (int(frobisher_alida.MD)),
             (int(frobisher_alida.MD + 10))):
                df_HS['HS_PSI'][i] = HS_300_low_rival
            

    for i in range(len(df_HS)): 
        if HS_300_low_rival == None:
            continue
        if df_HS['DEPTH'][i] in range(
             (int(frobisher_alida.MD) + 10),
             (int(frobisher_alida.MD + 130))):
                df_HS['HS_PSI'][i] = (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])
            
    for i in range(len(df_HS)):             
        if HS_upper_bakken == None:
            continue
        if df_HS['DEPTH'][i] in range(
             (int(upper_bakken.MD)),
             (int(upper_bakken.MD) + 160)):
                df_HS['HS_PSI'][i] = HS_upper_bakken 
            
                       
        
        
        
df_ovbd['OVBD_PPG'] = df_ovbd['OVBD_PSI'] / df_ovbd['DEPTH'] / 0.052
df_ovbd['Ts'] = None
df_ovbd['Ko'] = None

# df_ovbd = df_ovbd.replace({np.nan: None})
df_ovbd= df_ovbd.astype(float)        

shale = df_lith[df_lith['Lith'] == 'shale']
sand = df_lith[df_lith['Lith'] == 'sand']
limestone = df_lith[df_lith['Lith'] == 'limestone']
dolomite = df_lith[df_lith['Lith'] == 'dolomite']
anhydrite = df_lith[df_lith['Lith'] == 'anhydrite']
dolomitic_limestone = df_lith[df_lith['Lith'] == 'dolomitic limestone']
siltstone = df_lith[df_lith['Lith'] == 'siltstone']
    
    
# Create a function to iterate a loop to add Lithology, Ts, and Ko to the OVBD log
def FG_calcs():
    for i in range(len(df_ovbd)):
        if df_ovbd['DEPTH'][i] in range(
             (int(0)),
             (int(greenhorn.MD) + 20)):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(0)),
             (int(greenhorn.MD) + 20)):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]       



        if df_ovbd['DEPTH'][i] in range(
             (int(greenhorn.MD)),
             (int(greenhorn.MD) + 80)):
                      df_ovbd['Ko'][i] = sand['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(greenhorn.MD)),
             (int(greenhorn.MD) + 80)):
                      df_ovbd['Ts'][i] = sand['Ts'].values[0]   



        if df_ovbd['DEPTH'][i] in range(
             (int(greenhorn.MD) + 80),
             (int(belle_fourche.MD))):
                      df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(greenhorn.MD) + 80),
             (int(belle_fourche.MD))):
                      df_ovbd['Ts'][i] = siltstone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(belle_fourche.MD)),
             (int(mowry.MD) + 200)):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(belle_fourche.MD)),
             (int(mowry.MD) + 200)):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]  


        if df_ovbd['DEPTH'][i] in range(
             (int(mowry.MD)),
             (int(inyan_kara.MD))):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(mowry.MD)),
             (int(inyan_kara.MD))):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(inyan_kara.MD)),
             (int(swift.MD))):
                      df_ovbd['Ko'][i] = sand['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(inyan_kara.MD)),
             (int(swift.MD))):
                      df_ovbd['Ts'][i] = sand['Ts'].values[0]    


        if df_ovbd['DEPTH'][i] in range(
             (int(swift.MD)),
             (int(swift.MD) + 200)):
                      df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(swift.MD)),
             (int(swift.MD) + 200)):
                      df_ovbd['Ts'][i] = siltstone['Ts'].values[0]    



        if df_ovbd['DEPTH'][i] in range(
             (int(swift.MD) + 200),
             (int(rierdon.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(swift.MD) + 200),
             (int(rierdon.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



        if df_ovbd['DEPTH'][i] in range(
             (int(rierdon.MD)),
             (int(amsden.MD) - 20)):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(rierdon.MD)),
             (int(amsden.MD) - 20)):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



        if df_ovbd['DEPTH'][i] in range(
             (int(amsden.MD) - 20),
             (int(amsden.MD))):
                      df_ovbd['Ko'][i] = sand['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(amsden.MD) - 20),
             (int(amsden.MD))):
                      df_ovbd['Ts'][i] = sand['Ts'].values[0]   



        if df_ovbd['DEPTH'][i] in range(
             (int(amsden.MD)),
             (int(tyler.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(amsden.MD)),
             (int(tyler.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



        if df_ovbd['DEPTH'][i] in range(
             (int(tyler.MD)),
             (int(kibbey_lime.MD))):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(tyler.MD)),
             (int(kibbey_lime.MD))):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(kibbey_lime.MD)),
             (int(charles.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(kibbey_lime.MD)),
             (int(charles.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(charles.MD)),
             (int(top_last_salt.MD))):
                      df_ovbd['Ko'][i] = anhydrite['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(charles.MD)),
             (int(top_last_salt.MD))):
                      df_ovbd['Ts'][i] = anhydrite['Ts'].values[0]  




        if df_ovbd['DEPTH'][i] in range(
             (int(top_last_salt.MD)),
             (int(base_last_salt.MD))):
                      df_ovbd['Ko'][i] = anhydrite['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(top_last_salt.MD)),
             (int(base_last_salt.MD))):
                      df_ovbd['Ts'][i] = anhydrite['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(base_last_salt.MD)),
             (int(frobisher_alida.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(base_last_salt.MD)),
             (int(frobisher_alida.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(frobisher_alida.MD)),
             (int(lodgepole.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(frobisher_alida.MD)),
             (int(lodgepole.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(lodgepole.MD)),
             (int(upper_bakken.MD))):
                      df_ovbd['Ko'][i] = limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(lodgepole.MD)),
             (int(upper_bakken.MD))):
                      df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(upper_bakken.MD)),
             (int(middle_bakken.MD))):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(upper_bakken.MD)),
             (int(middle_bakken.MD))):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(middle_bakken.MD)),
             (int(lower_bakken.MD))):
                      df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(middle_bakken.MD)),
             (int(lower_bakken.MD))):
                      df_ovbd['Ts'][i] = siltstone['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(lower_bakken.MD)),
             (int(three_forks.MD))):
                      df_ovbd['Ko'][i] = shale['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(lower_bakken.MD)),
             (int(three_forks.MD))):
                      df_ovbd['Ts'][i] = shale['Ts'].values[0]  



        if df_ovbd['DEPTH'][i] in range(
             (int(three_forks.MD)),
             (int(birdbear.MD))):
                      df_ovbd['Ko'][i] = dolomitic_limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(three_forks.MD)),
             (int(birdbear.MD))):
                      df_ovbd['Ts'][i] = dolomitic_limestone['Ts'].values[0]  


        if df_ovbd['DEPTH'][i] in range(
             (int(birdbear.MD)),
             (int(birdbear.MD) + 3000)):
                      df_ovbd['Ko'][i] = dolomitic_limestone['Kf'].values[0]


        if df_ovbd['DEPTH'][i] in range(
             (int(birdbear.MD)),
             (int(birdbear.MD) + 3000)):
                      df_ovbd['Ts'][i] = dolomitic_limestone['Ts'].values[0]  



 
                 
    

st.set_page_config(layout="wide")

# Functions for each of the pages
def home(uploaded_file):
    if uploaded_file:
        st.header('Begin exploring the data using the menu on the left')
    else:
        st.header('To begin please upload a file')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df_ovbd.describe())

def topset_data():
        st.header('Uploaded Topset Data')
        st.write(df_topset)
    
def data_header():
    st.header('Header of Dataframe')
    st.write(df_ovbd.head())

# def displayplot():
#     st.header('Plot of Data')
    
#     fig, ax = plt.subplots(1,1)
#     ax.scatter(x=df_ovbd['Depth'], y=df_ovbd['Magnitude'])
#     ax.set_xlabel('Depth')
#     ax.set_ylabel('Magnitude')
    
#     st.pyplot(fig)

    
    
    
    
  
    
    
def interactive_plot():
    global df_ovbd
    st.subheader('Input Known Depth and Pressure Variables Below')

# Execute the functins defined earlier for Low Side, Most Likely, and High Side    
    LS_calcs()
    ML_calcs()
    HS_calcs()
    FG_calcs()

# Add a calculated column for PPG    
    df_LS['LS_PPG'] = df_LS['LS_PSI'] / df_LS['DEPTH'] / .052
    df_ML['ML_PPG'] = df_ML['ML_PSI'] / df_ML['DEPTH'] / .052
    df_HS['HS_PPG'] = df_HS['HS_PSI'] / df_HS['DEPTH'] / .052
    
# Create a column for Frac Gradient PSI and then create a column for Frac Gradient PPG with simple conversion
    df_ovbd['LS_FG_PSI'] = (df_ovbd['Ko']) * (df_ovbd['OVBD_PSI'] - df_LS['LS_PSI']) + df_LS['LS_PSI'] + df_ovbd['Ts']
    df_ovbd['LS_FG_PPG'] = df_ovbd['LS_FG_PSI'] / df_ovbd['DEPTH'] / 0.052
    df_ovbd['ML_FG_PSI'] = (df_ovbd['Ko']) * (df_ovbd['OVBD_PSI'] - df_ML['ML_PSI']) + df_ML['ML_PSI'] + df_ovbd['Ts']
    df_ovbd['ML_FG_PPG'] = df_ovbd['ML_FG_PSI'] / df_ovbd['DEPTH'] / 0.052 
    df_ovbd['HS_FG_PSI'] = (df_ovbd['Ko']) * (df_ovbd['OVBD_PSI'] - df_HS['HS_PSI']) + df_HS['HS_PSI'] + df_ovbd['Ts']
    df_ovbd['HS_FG_PPG'] = df_ovbd['HS_FG_PSI'] / df_ovbd['DEPTH'] / 0.052   
    
    col1, col2 = st.columns(2)

    # Standard Variables
    with col1.expander('Elevations and Base Zones'):
        st.write(
            Water_Table_Elev = st.number_input('Water Table Elevation',value = 100), #100.0
            Seabed_Elev = st.number_input('Seabed Elevation',value = 200), #200
            Base_Zone_1 = st.number_input('Base Zone 1',value = 14000), #14000
            Base_Zone_2 = st.number_input('Base Zone 2',value = 14000), #14000
            Base_Zone_3 = st.number_input('Base Zone 3',value = 15000), #15000
            Base_Zone_4 = st.number_input('Base Zone 4',value = 16000), #16000
            Base_Zone_5 = st.number_input('Base Zone 5',value = 17000), #17000
        )
        
    col1, col2, col3 = st.columns(3)    
    with col1.expander('Low Side Water Densities'):
        st.write(
            LS_Sea_Water_Density = st.number_input('LS Sea Water Density',value = 0.45), #0.45
            LS_Formation_water_Density_1 = st.number_input('LS Formation Water Density 1',value = 0.45), #0.45
            LS_Formation_water_Density_2 = st.number_input('LS Formation Water Density 2',value = 0.45), #0.45 
            LS_Formation_water_Density_3 = st.number_input('LS Formation Water Density 3',value = 0.52), #0.52
            LS_Formation_water_Density_4 = st.number_input('LS Formation Water Density 4',value = 0.45), #0.45
            LS_Formation_water_Density_5 = st.number_input('LS Formation Water Density 5',value = 0.45), #0.45
        )

    with col2.expander('Most Likely Water Densities'):
        st.write(
            ML_Sea_Water_Density = st.number_input('ML Sea Water Density', value = 0.47), #0.47
            ML_Formation_water_Density_1 = st.number_input('ML Formation Water Density 1',value = 0.47), #0.47
            ML_Formation_water_Density_2 = st.number_input('ML Formation Water Density 2',value = 0.47), #0.47 
            ML_Formation_water_Density_3 = st.number_input('ML Formation Water Density 3',value = 0.52), #0.52
            ML_Formation_water_Density_4 = st.number_input('ML Formation Water Density 4',value = 0.47), #0.47
            ML_Formation_water_Density_5 = st.number_input('ML Formation Water Density 5',value = 0.47), #0.47
        )


    with col3.expander('High Side Water Densities'):
        st.write(
            HS_Sea_Water_Density = st.number_input('HS Sea Water Density', value = 0.49), #0.49
            HS_Formation_water_Density_1 = st.number_input('HS Formation Water Density 1',value = 0.49), #0.49
            HS_Formation_water_Density_2 = st.number_input('HS Formation Water Density 2',value = 0.49), #0.49 
            HS_Formation_water_Density_3 = st.number_input('HS Formation Water Density 3',value = 0.52), #0.52
            HS_Formation_water_Density_4 = st.number_input('HS Formation Water Density 4',value = 0.49), #0.49
            HS_Formation_water_Density_5 = st.number_input('HS Formation Water Density 5',value = 0.49), #0.49
        )



    col1, col2, col3 = st.columns(3)
    with col1.expander("Low Side Pore Pressure Inputs (PSI)"):
        st.write(
            LS_inyan_kara = st.number_input('Inyan Kara LS'),
            LS_amsden = st.number_input('Amsden LS'),
            LS_frobisher_alida_interval = st.number_input('Frobisher-Alida Interval LS'),
            LS_upper_bakken = st.number_input('Upper Bakken LS')
        )
    
    with col2.expander('Most Likely Pore Pressure Inputs (PSI)'):
        st.write(
            ML_inyan_kara = st.number_input('Inyan Kara ML'),
            ML_amsden = st.number_input('Amsden ML'),
            ML_frobisher_alida_interval = st.number_input('Frobisher-Alida ML'),
            ML_upper_bakken = st.number_input('Upper Bakken ML')
        )
        
    with col3.expander('High Side Pore Pressure Inputs (PSI)'):
        st.write(
            HS_inyan_kara = st.number_input('Inyan Kara HS'),
            HS_amsden = st.number_input('Amsden HS'),
            HS_frobisher_alida_interval = st.number_input('Frobisher-Alida HS'),
            HS_upper_bakken = st.number_input('Upper Bakken HS')
        )    
    

    plot = go.Figure()
    plot.add_trace(go.Scatter( x = df_ovbd["OVBD_PPG"], y = df_ovbd["DEPTH"], name = 'Overburden'))
    plot.add_trace(go.Scatter(x = df_LS['LS_PPG'], y = df_LS['DEPTH'], name = 'LS Pore Pressure'))
    plot.add_trace(go.Scatter(x = df_ML['ML_PPG'], y = df_ML['DEPTH'], name = 'ML Pore Pressure'))
    plot.add_trace(go.Scatter(x = df_HS['HS_PPG'], y = df_HS['DEPTH'], name = 'HS Pore Pressure'))
    plot.add_trace(go.Scatter(x = df_ovbd['LS_FG_PPG'], y = df_ovbd['DEPTH'], name = 'LS Frac Gradient'))
    plot.add_trace(go.Scatter(x = df_ovbd['ML_FG_PPG'], y = df_ovbd['DEPTH'], name = 'ML Frac Gradient'))
    plot.add_trace(go.Scatter(x = df_ovbd['HS_FG_PPG'], y = df_ovbd['DEPTH'], name = 'HS Frac Gradient'))

    plot.update_yaxes(autorange = 'reversed')
    plot.update_layout(title_text = 'Pore Pressure Log Plot', title_x = .5,  
                       height = 1200,
                          template='plotly_white')
    
# Add formation tops and labels
    greenhorn_upload = df_topset[df_topset['TopName'] == 'Greenhorn']
    belle_fourche_upload = df_topset[df_topset['TopName'] == 'Belle_Fourche']
    mowry_upload = df_topset[df_topset['TopName'] == 'Mowry']
    inyan_kara_upload = df_topset[df_topset['TopName'] == 'Inyan_Kara']
    swift_upload = df_topset[df_topset['TopName'] == 'Swift']
    rierdon_upload = df_topset[df_topset['TopName'] == 'Rierdon']
    amsden_upload = df_topset[df_topset['TopName'] == 'Amsden']
    tyler_upload = df_topset[df_topset['TopName'] == 'Tyler']
    kibbey_lime_upload = df_topset[df_topset['TopName'] == 'Kibbey_Lime']
    charles_upload = df_topset[df_topset['TopName'] == 'Charles']
    top_last_salt_upload = df_topset[df_topset['TopName'] == 'Top_Last_Salt']
    base_last_salt_upload = df_topset[df_topset['TopName'] == 'Base_Last_Salt']
    frobisher_alida_upload = df_topset[df_topset['TopName'] == 'Frobisher-Alida_Interval']
    lodgepole_upload = df_topset[df_topset['TopName'] == 'Lodgepole']
    upper_bakken_upload = df_topset[df_topset['TopName'] == 'Upper_Bakken']
    middle_bakken_upload = df_topset[df_topset['TopName'] == 'Middle_Bakken']
    lower_bakken_upload = df_topset[df_topset['TopName'] == 'Lower_Bakken']
    three_forks_upload = df_topset[df_topset['TopName'] == 'Three_Forks']
    birdbear_upload = df_topset[df_topset['TopName'] == 'Birdbear']      

    plot.add_hline(y = int(greenhorn_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Greenhorn', annotation_position = 'top left')
    plot.add_hline(y = int(greenhorn_upload['MD']) + 200, line_dash="dot", row=1, col="all", annotation_text = 'Greenhorn Silt', annotation_position = 'top left')
    plot.add_hline(y = int(mowry_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Mowry', annotation_position = 'top left')
    plot.add_hline(y = int(inyan_kara_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Inyan Kara', annotation_position = 'top left')
    plot.add_hline(y = int(swift_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Swift', annotation_position = 'top left')
    plot.add_hline(y = int(rierdon_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Rierdon', annotation_position = 'top left')
    plot.add_hline(y = int(amsden_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Amsden', annotation_position = 'top left')
    plot.add_hline(y = int(tyler_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Tyler', annotation_position = 'top left')
    plot.add_hline(y = int(kibbey_lime_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Kibbey Lime', annotation_position = 'top left')
    plot.add_hline(y = int(charles_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Charles', annotation_position = 'top left')
 #   plot.add_hline(y = int(top_last_salt_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Top Last Salt', annotation_position = 'top left')
 #   plot.add_hline(y = int(base_last_salt_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Base Last Salt', annotation_position = 'top left')
    plot.add_hline(y = int(frobisher_alida_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Frobisher Alida', annotation_position = 'top left')
    plot.add_hline(y = int(upper_bakken_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Upper Bakken Shale', annotation_position = 'top left')
 #   plot.add_hline(y = int(lower_bakken_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Lower Bakken Shale', annotation_position = 'top left')
    plot.add_hline(y = int(birdbear_upload['MD']), line_dash="dot", row=1, col="all", annotation_text = 'Birdbear', annotation_position = 'top left')

    st.plotly_chart(plot, use_container_width=True)



    
# Add a title and intro text
st.title('PPFG Data Explorer')
st.text('This is a web app to allow exploration of PPFG Data')

# Sidebar setup
st.sidebar.title('Sidebar')
upload_file = st.sidebar.file_uploader('Upload a file containing OVBD data')
upload_topset = st.sidebar.file_uploader('Upload a csv file containing Topset data')

#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', ['Home', 'Topset Data', 'Data Summary', 'Data Header', 'Scatter Plot', 'Jacob Plots'])

# Check if file has been uploaded
if upload_file is not None:
    df_ovbd = pd.read_csv(upload_file)
    
if upload_topset is not None:
    df_topset = pd.read_csv(upload_topset)    

# Navigation options
if options == 'Home':
    home(upload_file)
    
elif options == 'Topset Data':
    topset_data()
    
elif options == 'Data Summary':
    data_summary()
    
elif options == 'Data Header':
    data_header()
    
# elif options == 'Scatter Plot':
#     displayplot()
    
elif options == 'Jacob Plots':
    interactive_plot()


