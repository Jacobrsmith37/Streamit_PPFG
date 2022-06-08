#!pip install streamlit
#Import the required Libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import lasio
from PIL import Image

image_logo = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Logo.png')
image_ship = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Drill_Ship.jpg')
image_bakken_rig = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Bakken_Rig.jpg')

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


# # Bring in topset and remove last column
# Topset1 = pd.read_csv('Topset1_Updated_PPFG.csv')#, sep = "\t")
# Topset1.drop('GeosteeringDip', axis = 1, inplace = True)

# Topset1['TopName'] = Topset1['TopName'].str.title()


        
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
    
    



st.set_page_config(layout="wide")

# Functions for each of the pages
def home():
    st.header('Begin exploring the data using the menu on the left')
    st.image(image_bakken_rig)
    st.subheader('To begin, upload a Topset csv file, then navigate to  "'"Jacob Plots"'" on the Sidebar')

def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df_ovbd.describe())

def topset_data():
        st.header('Uploaded Topset Data')
        st.dataframe(df_topset)

def lith_data():
        st.header('Lithology-Based Geomechanical Properties')
        st.write(df_lith)
        
    
def interactive_plot():
    global df_ovbd
    st.subheader('Input Known Depth and Pressure Variables Below')
    st.info('*** 0 is equal to an ignored value ***')

# Standard Variables  
    col1, col2 = st.columns(2)
    with col1.expander('Elevations and Base Zones'):
        if 'Water Table Elevation' not in st.session_state:
            #st.session_state.Water_Table_Elev = 0
            Water_Table_Elev = st.number_input('Water Table Elevation', value = 100)   
        
        if 'Seabed Elevation' not in st.session_state:
            #st.session_state.Seabed_Elev = 0
            Seabed_Elev = st.number_input('Seabed Elevation', value = 200)
         
        if 'Base Zone 1' not in st.session_state:
            #st.session_state.Base_Zone_1 = 0
            Base_Zone_1 = st.number_input('Base Zone 1', value = 14000)
          
        if 'Base Zone 2' not in st.session_state:
            Base_Zone_2 = st.number_input('Base Zone 2', value = 14000)
            
        if 'Base Zone 3' not in st.session_state:
            Base_Zone_3 = st.number_input('Base Zone 3', value = 15000)
            
        if 'Base Zone 4' not in st.session_state:
            Base_Zone_4 = st.number_input('Base Zone 4', value = 16000)
            
        if 'Base Zone 5' not in st.session_state:
            Base_Zone_5 = st.number_input('Base Zone 5', value = 17000)#  if Base_Zone_1:    


    col1, col2, col3 = st.columns(3)    
    with col1.expander('Low Side Water Densities'):
        if 'Low Side Sea_Water_Density' not in st.session_state:
            LS_Sea_Water_Density = st.number_input('Low Side Sea Water Density', step = 1e-2, value = .45)  
        if 'Low Side Formation Water Density 1' not in st.session_state:
            LS_Formation_water_Density_1 = st.number_input('Low Side Formation Water Density 1', step = 1e-2, value = .45)
        if 'Low Side Formation Water Density 2' not in st.session_state:
            LS_Formation_water_Density_2 = st.number_input('Low Side Formation Water Density 2', step = 1e-2, value = .45)  
        if 'Low Side Formation Water Density 3' not in st.session_state:
            LS_Formation_water_Density_3 = st.number_input('Low Side Formation Water Density 3', step = 1e-2, value = .52)  
        if 'Low Side Formation Water Density 4' not in st.session_state:
            LS_Formation_water_Density_4 = st.number_input('Low Side Formation Water Density 4', step = 1e-2, value = .45)  
        if 'Low Side Formation Water Density 5' not in st.session_state:
            LS_Formation_water_Density_5 = st.number_input('Low Side Formation Water Density 5', step = 1e-2, value = .45)  
            

    with col2.expander('Most Likely Water Densities'):
        if 'Most Likely Sea Water Density' not in st.session_state:
            ML_Sea_Water_Density = st.number_input('Most Likely Sea Water Density', step = 1e-2, value = .47)  
        if 'Most Likely Formation Water Density 1' not in st.session_state:
            ML_Formation_water_Density_1 = st.number_input('Most Likely Formation Water Density 1', step = 1e-2, value = .47)
        if 'Most Likely Formation Water Density 2' not in st.session_state:
            ML_Formation_water_Density_2 = st.number_input('Most Likely Formation Water Density 2', step = 1e-2, value = .47)  
        if 'Most Likely Formation Water Density 3' not in st.session_state:
            ML_Formation_water_Density_3 = st.number_input('Most Likely Formation Water Density 3', step = 1e-2, value = .52)  
        if 'Most Likely Formation Water Density 4' not in st.session_state:
            ML_Formation_water_Density_4 = st.number_input('Most Likely Formation Water Density 4', step = 1e-2, value = .47)  
        if 'Most Likely Formation Water Density 5' not in st.session_state:
            ML_Formation_water_Density_5 = st.number_input('Most Likely Formation Water Density 5', step = 1e-2, value = .47)  


    with col3.expander('High Side Water Densities'):
        if 'High Side Sea Water Density' not in st.session_state:
            HS_Sea_Water_Density = st.number_input('High Side Sea Water Density', step = 1e-2, value = .49)  
        if 'High Side Formation Water Density 1' not in st.session_state:
            HS_Formation_water_Density_1 = st.number_input('High Side Formation Water Density 1', step = 1e-2, value = .49)
        if 'High Side Formation Water Density 2' not in st.session_state:
            HS_Formation_water_Density_2 = st.number_input('High Side Formation Water Density 2', step = 1e-2, value = .49)  
        if 'High Side Formation Water Density 3' not in st.session_state:
            HS_Formation_water_Density_3 = st.number_input('High Side Formation Water Density 3', step = 1e-2, value = .52)  
        if 'High Side Formation Water Density 4' not in st.session_state:
            HS_Formation_water_Density_4 = st.number_input('High Side Formation Water Density 4', step = 1e-2, value = .49)  
        if 'High Side Formation Water Density 5' not in st.session_state:
            HS_Formation_water_Density_5 = st.number_input('High Side Formation Water Density 5', step = 1e-2, value = .49)  
            

    col1, col2, col3 = st.columns(3)
    with col1.expander("Low Side Pore Pressure Inputs (PSI)"):
        if 'Low Side Inyan Kara' not in st.session_state:
            LS_inyan_kara = st.number_input('Low Side Inyan Kara', value = 3200)
        if 'Low Side Amsden' not in st.session_state:
            LS_20_high_amsden = st.number_input('Low Side Amsden', value = 0)  
        if 'Low Side Frobisher-Alida' not in st.session_state:
            LS_300_low_rival = st.number_input('Low Side Frobisher-Alida', value = 0)  
        if 'Low Side Upper Bakken' not in st.session_state:
            LS_upper_bakken = st.number_input('Low Side Upper Bakken', value = 8400)  
            

    with col2.expander('Most Likely Pore Pressure Inputs (PSI)'):
        if 'Most Likely Inyan Kara' not in st.session_state:
            ML_inyan_kara = st.number_input('Most Likely Inyan Kara', value = 3600)
        if 'Most Likely Amsden' not in st.session_state:
            ML_20_high_amsden = st.number_input('Most Likely Amsden', value = 0)  
        if 'Most Likely Frobisher-Alida' not in st.session_state:
            ML_300_low_rival = st.number_input('Most Likely Frobisher-Alida', value = 0)  
        if 'Most Likely Upper Bakken' not in st.session_state:
            ML_upper_bakken = st.number_input('Most Likely Upper Bakken', value = 8850)  
            
            
    with col3.expander('High Side Pore Pressure Inputs (PSI)'):
        if 'High Side Inyan Kara' not in st.session_state:
            HS_inyan_kara = st.number_input('High Side Inyan Kara', value = 3700)
        if 'High Side Amsden' not in st.session_state:
            HS_20_high_amsden = st.number_input('High Side Amsden', value = 0)  
        if 'High Side Frobisher-Alida' not in st.session_state:
            HS_300_low_rival = st.number_input('High Side Frobisher-Alida', value = 0)  
        if 'High Side Upper Bakken' not in st.session_state:
            HS_upper_bakken = st.number_input('High Side Upper Bakken', value = 9200)  
            


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

            if LS_inyan_kara == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                  (int(inyan_kara_upload.MD)),
                  (int(inyan_kara_upload.MD) + 20)):
                     df_LS['LS_PSI'][i] = LS_inyan_kara

        for i in range(len(df_LS)):                
            if LS_inyan_kara == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD) + 20),
                 (int(swift_upload.MD))):
                    df_LS['LS_PSI'][i] =  (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1])  


        for i in range(len(df_LS)):
            if LS_20_high_amsden == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                 (int(amsden_upload.MD) - 20),
                 (int(amsden_upload.MD) + 0)):
                     df_LS['LS_PSI'][i] = LS_20_high_amsden

        for i in range(len(df_LS)):            
            if LS_300_low_rival == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(frobisher_alida_upload.MD) - 10),
                (int(frobisher_alida_upload.MD) + 10)):
                     df_LS['LS_PSI'][i] = LS_300_low_rival



        for i in range(len(df_LS)):     
            if LS_300_low_rival == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(frobisher_alida_upload.MD) + 10),
                (int(frobisher_alida_upload.MD) + 130)):
                    df_LS['LS_PSI'][i] = (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1]) 

        for i in range(len(df_LS)):            
            if LS_upper_bakken == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(upper_bakken_upload.MD) + 0),
                (int(upper_bakken_upload.MD) + 160)):
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
            if ML_inyan_kara == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD)),
                 (int(inyan_kara_upload.MD) + 20)):
                    df_ML['ML_PSI'][i] = ML_inyan_kara

        for i in range(len(df_ML)):                 
            if ML_inyan_kara == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD) + 20),
                 (int(swift_upload.MD))):
                    df_ML['ML_PSI'][i] =  (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])     

        for i in range(len(df_ML)):                 
            if ML_20_high_amsden == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(amsden_upload.MD) - 20),
                 (int(amsden_upload.MD) + 0)):
                    df_ML['ML_PSI'][i] = ML_20_high_amsden 

        for i in range(len(df_ML)):                 
            if ML_300_low_rival == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD) - 10),
                 (int(frobisher_alida_upload.MD + 10))):
                    df_ML['ML_PSI'][i] = ML_300_low_rival

        for i in range(len(df_ML)):                 
            if ML_300_low_rival == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD) + 10),
                 (int(frobisher_alida_upload.MD + 130))):
                    df_ML['ML_PSI'][i] = (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])   

        for i in range(len(df_ML)):                 
            if ML_upper_bakken == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(upper_bakken_upload.MD)),
                 (int(upper_bakken_upload.MD) + 160)):
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
            if HS_inyan_kara == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD)),
                 (int(inyan_kara_upload.MD) + 20)):
                    df_HS['HS_PSI'][i] = HS_inyan_kara

        for i in range(len(df_HS)):                 
            if HS_inyan_kara == 0:
                    continue
            if df_HS['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD) + 20),
                 (int(swift_upload.MD))):
                    df_HS['HS_PSI'][i] =  (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])

        for i in range(len(df_HS)):                 
            if HS_20_high_amsden == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(amsden_upload.MD) - 20),
                 (int(amsden_upload.MD) + 0)):
                    df_HS['HS_PSI'][i] = HS_20_high_amsden 

        for i in range(len(df_HS)):                 
            if HS_300_low_rival == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD)),
                 (int(frobisher_alida_upload.MD + 10))):
                    df_HS['HS_PSI'][i] = HS_300_low_rival


        for i in range(len(df_HS)): 
            if HS_300_low_rival == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD) + 10),
                 (int(frobisher_alida_upload.MD + 130))):
                    df_HS['HS_PSI'][i] = (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])

        for i in range(len(df_HS)):             
            if HS_upper_bakken == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(upper_bakken_upload.MD)),
                 (int(upper_bakken_upload.MD) + 160)):
                    df_HS['HS_PSI'][i] = HS_upper_bakken      

                
                
# Create a function to iterate a loop to add Lithology, Ts, and Ko to the OVBD log
    def FG_calcs():
        for i in range(len(df_ovbd)):
            if df_ovbd['DEPTH'][i] in range(
                 (int(0)),
                 (int(greenhorn_upload.MD) + 20)):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(0)),
                 (int(greenhorn_upload.MD) + 20)):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]       



            if df_ovbd['DEPTH'][i] in range(
                 (int(greenhorn_upload.MD)),
                 (int(greenhorn_upload.MD) + 80)):
                          df_ovbd['Ko'][i] = sand['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(greenhorn_upload.MD)),
                 (int(greenhorn_upload.MD) + 80)):
                          df_ovbd['Ts'][i] = sand['Ts'].values[0]   



            if df_ovbd['DEPTH'][i] in range(
                 (int(greenhorn_upload.MD) + 80),
                 (int(belle_fourche_upload.MD))):
                          df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(greenhorn_upload.MD) + 80),
                 (int(belle_fourche_upload.MD))):
                          df_ovbd['Ts'][i] = siltstone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(belle_fourche_upload.MD)),
                 (int(mowry_upload.MD) + 200)):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(belle_fourche_upload.MD)),
                 (int(mowry_upload.MD) + 200)):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]  


            if df_ovbd['DEPTH'][i] in range(
                 (int(mowry_upload.MD)),
                 (int(inyan_kara_upload.MD))):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(mowry_upload.MD)),
                 (int(inyan_kara_upload.MD))):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD)),
                 (int(swift_upload.MD))):
                          df_ovbd['Ko'][i] = sand['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(inyan_kara_upload.MD)),
                 (int(swift_upload.MD))):
                          df_ovbd['Ts'][i] = sand['Ts'].values[0]    


            if df_ovbd['DEPTH'][i] in range(
                 (int(swift_upload.MD)),
                 (int(swift_upload.MD) + 200)):
                          df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(swift_upload.MD)),
                 (int(swift_upload.MD) + 200)):
                          df_ovbd['Ts'][i] = siltstone['Ts'].values[0]    



            if df_ovbd['DEPTH'][i] in range(
                 (int(swift_upload.MD) + 200),
                 (int(rierdon_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(swift_upload.MD) + 200),
                 (int(rierdon_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



            if df_ovbd['DEPTH'][i] in range(
                 (int(rierdon_upload.MD)),
                 (int(amsden_upload.MD) - 20)):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(rierdon_upload.MD)),
                 (int(amsden_upload.MD) - 20)):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



            if df_ovbd['DEPTH'][i] in range(
                 (int(amsden_upload.MD) - 20),
                 (int(amsden_upload.MD))):
                          df_ovbd['Ko'][i] = sand['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(amsden_upload.MD) - 20),
                 (int(amsden_upload.MD))):
                          df_ovbd['Ts'][i] = sand['Ts'].values[0]   



            if df_ovbd['DEPTH'][i] in range(
                 (int(amsden_upload.MD)),
                 (int(tyler_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(amsden_upload.MD)),
                 (int(tyler_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]   



            if df_ovbd['DEPTH'][i] in range(
                 (int(tyler_upload.MD)),
                 (int(kibbey_lime_upload.MD))):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(tyler_upload.MD)),
                 (int(kibbey_lime_upload.MD))):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(kibbey_lime_upload.MD)),
                 (int(charles_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(kibbey_lime_upload.MD)),
                 (int(charles_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(charles_upload.MD)),
                 (int(top_last_salt_upload.MD))):
                          df_ovbd['Ko'][i] = anhydrite['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(charles_upload.MD)),
                 (int(top_last_salt_upload.MD))):
                          df_ovbd['Ts'][i] = anhydrite['Ts'].values[0]  




            if df_ovbd['DEPTH'][i] in range(
                 (int(top_last_salt_upload.MD)),
                 (int(base_last_salt_upload.MD))):
                          df_ovbd['Ko'][i] = anhydrite['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(top_last_salt_upload.MD)),
                 (int(base_last_salt_upload.MD))):
                          df_ovbd['Ts'][i] = anhydrite['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(base_last_salt_upload.MD)),
                 (int(frobisher_alida_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(base_last_salt_upload.MD)),
                 (int(frobisher_alida_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD)),
                 (int(lodgepole_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.MD)),
                 (int(lodgepole_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(lodgepole_upload.MD)),
                 (int(upper_bakken_upload.MD))):
                          df_ovbd['Ko'][i] = limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(lodgepole_upload.MD)),
                 (int(upper_bakken_upload.MD))):
                          df_ovbd['Ts'][i] = limestone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(upper_bakken_upload.MD)),
                 (int(middle_bakken_upload.MD))):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(upper_bakken_upload.MD)),
                 (int(middle_bakken_upload.MD))):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(middle_bakken_upload.MD)),
                 (int(lower_bakken_upload.MD))):
                          df_ovbd['Ko'][i] = siltstone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(middle_bakken_upload.MD)),
                 (int(lower_bakken_upload.MD))):
                          df_ovbd['Ts'][i] = siltstone['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(lower_bakken_upload.MD)),
                 (int(three_forks_upload.MD))):
                          df_ovbd['Ko'][i] = shale['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(lower_bakken_upload.MD)),
                 (int(three_forks_upload.MD))):
                          df_ovbd['Ts'][i] = shale['Ts'].values[0]  



            if df_ovbd['DEPTH'][i] in range(
                 (int(three_forks_upload.MD)),
                 (int(birdbear_upload.MD))):
                          df_ovbd['Ko'][i] = dolomitic_limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(three_forks_upload.MD)),
                 (int(birdbear_upload.MD))):
                          df_ovbd['Ts'][i] = dolomitic_limestone['Ts'].values[0]  


            if df_ovbd['DEPTH'][i] in range(
                 (int(birdbear_upload.MD)),
                 (int(birdbear_upload.MD) + 3000)):
                          df_ovbd['Ko'][i] = dolomitic_limestone['Kf'].values[0]


            if df_ovbd['DEPTH'][i] in range(
                 (int(birdbear_upload.MD)),
                 (int(birdbear_upload.MD) + 3000)):
                          df_ovbd['Ts'][i] = dolomitic_limestone['Ts'].values[0]  

# Add formation tops and labels
    greenhorn_upload = df_topset[df_topset['TopName'] == 'GREENHORN']
    belle_fourche_upload = df_topset[df_topset['TopName'] == 'BELLE_FOURCHE']
    mowry_upload = df_topset[df_topset['TopName'] == 'MOWRY']
    inyan_kara_upload = df_topset[df_topset['TopName'] == 'INYAN_KARA']
    swift_upload = df_topset[df_topset['TopName'] == 'SWIFT']
    rierdon_upload = df_topset[df_topset['TopName'] == 'RIERDON']
    amsden_upload = df_topset[df_topset['TopName'] == 'AMSDEN']
    tyler_upload = df_topset[df_topset['TopName'] == 'TYLER']
    kibbey_lime_upload = df_topset[df_topset['TopName'] == 'KIBBEY_LIME']
    charles_upload = df_topset[df_topset['TopName'] == 'CHARLES']
    top_last_salt_upload = df_topset[df_topset['TopName'] == 'TOP_LAST_SALT']
    base_last_salt_upload = df_topset[df_topset['TopName'] == 'BASE_LAST_SALT']
    frobisher_alida_upload = df_topset[df_topset['TopName'] == 'FROBISHER-ALIDA_INTERVAL']
    lodgepole_upload = df_topset[df_topset['TopName'] == 'LODGEPOLE']
    upper_bakken_upload = df_topset[df_topset['TopName'] == 'UPPER_BAKKEN_SHALE']
    middle_bakken_upload = df_topset[df_topset['TopName'] == 'MIDDLE_BAKKEN']
    lower_bakken_upload = df_topset[df_topset['TopName'] == 'LOWER_BAKKEN_SHALE']
    three_forks_upload = df_topset[df_topset['TopName'] == 'THREE_FORKS']
    birdbear_upload = df_topset[df_topset['TopName'] == 'BIRDBEAR']  
    
# Execute the functions defined earlier for Low Side, Most Likely, and High Side    
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
                          template='plotly')
    
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
st.sidebar.image(image_logo)
#st.sidebar.title('Sidebar')
# upload_file = st.sidebar.file_uploader('Upload a file containing OVBD data')
upload_topset = st.sidebar.file_uploader('Upload a csv file containing Topset data')

#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', ['Home', 'Topset Data', 'Lithology Data', 'Jacob Plots'])

# Check if file has been uploaded
# if upload_file is not None:
#     df_ovbd = pd.read_csv(upload_file)
    
if upload_topset is not None:
    df_topset = pd.read_csv(upload_topset)
  
    
# Navigation options
if options == 'Home':
    home()
    
elif options == 'Topset Data':
    topset_data()
    
elif options == 'Lithology Data':
    lith_data()
    
elif options == 'Data Summary':
    data_summary()
    
# elif options == 'Data Header':
#     data_header()
    
# elif options == 'Scatter Plot':
#     displayplot()
    
elif options == 'Jacob Plots':
    interactive_plot()

