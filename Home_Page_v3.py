#!pip install streamlit
#pip install streamlit-aggrid
#pip install --upgrade streamlit
#Import the required Libraries
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import lasio
from PIL import Image
from st_aggrid import AgGrid
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
import time



#Run the app locally
#Streamlit run C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Python\my_app\Home_Page.py

# #    Turn to code for Web Service  
# ######################################
image_logo = Image.open('Hess_Logo.png')
image_bakken_rig = Image.open('Hess_Bakken_Rig.jpg')

# read the las file and show the headers, or 'keys'
las = lasio.read("OVBD_PSI.las")
# #######################################




#    Turn to code for Local Host  
#######################################
# image_logo = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Logo.png')
# image_ship = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Drill_Ship.jpg')
# image_bakken_rig = Image.open(r'C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Hess_Bakken_Rig.jpg')

# # read the las file and show the headers, or 'keys'
# las = lasio.read(r"C:\Users\jac84753\OneDrive\Documents\Jacob\HESS\Pore Pressure\OVBD_PSI.las")
#######################################


# Add a title and intro text
st.title('PPFG Data Explorer')
st.text('This is a web app to allow exploration of PPFG Data')

# Sidebar setup
st.sidebar.image(image_logo)

upload_topset = st.sidebar.file_uploader('Upload a csv file containing Topset data')


  

if upload_topset is not None:
    df_topset = pd.read_csv(upload_topset)
else: st.warning('Upload your Topset (must include TVD values)')    
    

        
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



# Functions
def home():
    st.header('Begin exploring the data below')
    st.image(image_bakken_rig)
    st.subheader('To begin, upload a Topset csv file on the Sidebar')

options = st.sidebar.radio('View Mud Weight/Pressure Calculator', ['No', 'Yes'])
def calc():

    st.write('Mud Weight to PSI Calculator')

    def ppg_to_psi():
        st.session_state.psi = st.session_state.ppg * st.session_state.depth * .052

    def psi_to_ppg():
        st.session_state.ppg = st.session_state.psi / st.session_state.depth / .052

    def depth():
        st.session_state.depth 

    def clear():
        st.session_state.depth, st.session_state.psi, st.session_state.ppg = 0,0,0


    col1, buff, col2 = st.columns([2,1,2])
    with col1:
        Depth = st.number_input('Depth (ft)' , key = 'depth')


    with st.container():   
        col1, buff, col2 = st.columns([2,1,2])
        with col1:
            Mud = st.number_input('Mud Weight (PPG)' , key = 'ppg',
                                 on_change = ppg_to_psi)



        with col2:
            Pressure = st.number_input('Formation Pressure (PSI):' , key = 'psi',
                                      on_change = psi_to_ppg)    

    st.button('Clear Inputs', on_click = clear)        

    
    
   #added 02/21/2023 
options_2 = st.sidebar.radio('Troubleshooting?', ['No', 'Yes'])
def troubleshooting():

    st.subheader('Common Errors and How to Fix Them')
    st.write('- Your topset should have a minimum of 3 colums: "TopName", "TVD", and either "MD" or "Lithology" or whatever you would like')
    st.write('- TopNames must be spelled correctly with appropriate underscores, etc.. Example: change "Rival" to "Frobisher-Alida_Interval"')
    st.write('- If you change a pressure on the bottom containers and get an error, check that your Topset names are spelled correctly and are present. These will match the standard Petrel nomenclature eg LOWER_BAKKEN_SHALE and INYAN_KARA')
    st.write('- If you want to differentiate Inyan Kara into 2 lobes with different pressures, ensure you add a top called "Inyan_Kara_2" and a TVD before you drag and drop your topset')
    st.write('- Lithology needs to be lowercase. You can add any you need with the Add Lithology function, but the standards built in are: *shale, sand, limestone, dolomite, anhydrite, dolomitic limestone, siltstone, coal*')
    
    
    
def interactive_plot():
    global df_topset
    global df_ovbd
    global df_lith
    st.write('Here is your uploaded and editable Topset:')
    

    df_topset.fillna(0, inplace=True)
    df_topset = df_topset.astype({"TVD":"int"})
    df_append = pd.DataFrame([[0] * len(df_topset.columns)], columns = df_topset.columns)
    df_append.loc[0:1,'TopName'] = 'GROUND LEVEL'
    df_append.loc[0:1,'TVD'] = 32
    df_append.loc[0:1,'Lithology'] = 'sand'
    df_topset = pd.concat([df_append, df_topset], ignore_index = True)
    
   
    
    if 'Lithology' not in df_topset:
        df_topset.insert(3, 'Lithology', '')
    if 'Plot?' not in df_topset:
        df_topset.insert(4, 'Plot?', '')
          

    options = GridOptionsBuilder.from_dataframe(
        
        df_topset, 
        editable = True,
        enableRowGroup = True, 
        enableValue = True, 
        enablePivot = True
        )

    options.configure_side_bar()
    options.configure_selection("single")

    df_topset = AgGrid(df_topset,
                       editable = True,
                       enable_enterprise_modules = True,
                       gridOptions = options.build(), 
                       update_mode = GridUpdateMode.MODEL_CHANGED,
                       fit_columns_on_grid_load = False,
                       allow_unsafe_jscode = True)
    #df_topset = AgGrid(df_topset, editable = True)
    new_df = df_topset['data']   
   
    
    def convert_df(new_df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return new_df.to_csv().encode('utf-8')
    st.download_button(
     label = "Download Topset Data as CSV",
     data = convert_df(new_df),
     file_name = 'Topset_PPFG_Export.csv',
     mime = 'csv'
 ) 
    
    
    
    
    
    st.header('Lithology-Based Geomechanical Properties') 
    
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
    df_lith = pd.DataFrame(data, columns = ['Lithology', 'Kf', 'Ts'])
    
    if "df_lith" not in st.session_state:
        st.session_state.df_lith = pd.DataFrame(data, columns = ['Lithology', 'Kf', 'Ts'])

    st.subheader("Add Lithology")

    num_new_rows = 50
    ncol = st.session_state.df_lith.shape[1]  # col count
    rw = -1
    
    st.session_state.df_lith = st.session_state.df_lith.astype(dtype= {"Lithology":"str", "Kf":"str", "Ts":"str"})
    
    with st.form(key="add form", clear_on_submit= True):
        cols = st.columns(ncol)
        rwdta = []

        for i in range(ncol):
            rwdta.append(cols[i].text_input(st.session_state.df_lith.columns[i]))

        if st.form_submit_button("Add"):
            if st.session_state.df_lith.shape[0] == num_new_rows:
                st.error("Add row limit reached. Cant add any more records..")
            else:
                rw = st.session_state.df_lith.shape[0] + 1
                st.info(f"Row: {rw} / {num_new_rows} added")
                st.session_state.df_lith.loc[rw] = rwdta

                if st.session_state.df_lith.shape[0] == num_new_rows:
                    st.error("Add row limit reached...")

    df_lith = st.session_state.df_lith    

        
        
    options = GridOptionsBuilder.from_dataframe(
        df_lith, 
        editable = True,
        enableRowGroup = True, 
        enableValue = True, 
        enablePivot = True
        )

    options.configure_side_bar()
    options.configure_selection("single")

    df_lith = AgGrid(
        df_lith,
        editable = True,
        enable_enterprise_modules = True,
        gridOptions = options.build(), 
        update_mode = GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load = False,
        allow_unsafe_jscode = True)
    
    df_lith = df_lith['data'] 
    

    
    merge_df = pd.merge(new_df, df_lith, on = ['Lithology'], how = 'inner')
    merge_df = merge_df[['TopName', 'TVD', 'Lithology', 'Kf', 'Ts', 'Plot?']].sort_values(by = ['TVD'], ascending = True)
#     merge_df = merge_df.astype(str)
 
    
    
    
    st.subheader('Merged Dataframe Ouput (not editable)')
    st.write('The graph will plot based on this dataframe')
    options = GridOptionsBuilder.from_dataframe(
        merge_df, 
        editable = False,
        enableRowGroup = True, 
        enableValue = True, 
        enablePivot = True
        )
    options.configure_side_bar()
    options.configure_selection("single")
    
    merge_df = AgGrid(merge_df, editable = False, 
        enable_enterprise_modules = True,
        gridOptions = options.build(), 
        update_mode = GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load = False,
        allow_unsafe_jscode = True)

    merge_df = merge_df['data'] 

    
    
    
    df_ovbd['OVBD_PPG'] = df_ovbd['OVBD_PSI'] / df_ovbd['DEPTH'] / 0.052
    df_ovbd['Ts'] = None
    df_ovbd['Ko'] = None

    # df_ovbd = df_ovbd.replace({np.nan: None})
    df_ovbd= df_ovbd.astype(float)        

    shale = df_lith[df_lith['Lithology'] == 'shale']
    sand = df_lith[df_lith['Lithology'] == 'sand']
    limestone = df_lith[df_lith['Lithology'] == 'limestone']
    dolomite = df_lith[df_lith['Lithology'] == 'dolomite']
    anhydrite = df_lith[df_lith['Lithology'] == 'anhydrite']
    dolomitic_limestone = df_lith[df_lith['Lithology'] == 'dolomitic limestone']
    siltstone = df_lith[df_lith['Lithology'] == 'siltstone']
    
    
   
    
    
    with st.spinner(text='Calculating Log Curves...'):
        time.sleep(2)
        st.success('Done Calculating... Rendering Interactive Plot')
   
    st.subheader('Input Known Depth and Pressure Variables Below')
    st.info('*** 0 is equal to an ignored value ***')

# Standard Variables  
    col1, col2 = st.columns(2)
    with col1.expander('Elevations and Base Zones'):
        if 'Water Table Elevation' not in st.session_state:
            Water_Table_Elev = st.number_input('Water Table Elevation', value = 100)   
        
        if 'Seabed Elevation' not in st.session_state:
            Seabed_Elev = st.number_input('Seabed Elevation', value = 200)
         
        if 'Base Zone 1' not in st.session_state:
            Base_Zone_1 = st.number_input('Base Zone 1', value = 14000)
          
        if 'Base Zone 2' not in st.session_state:
            Base_Zone_2 = st.number_input('Base Zone 2', value = 14000)
            
        if 'Base Zone 3' not in st.session_state:
            Base_Zone_3 = st.number_input('Base Zone 3', value = 15000)
            
        if 'Base Zone 4' not in st.session_state:
            Base_Zone_4 = st.number_input('Base Zone 4', value = 16000)
            
        if 'Base Zone 5' not in st.session_state:
            Base_Zone_5 = st.number_input('Base Zone 5', value = 17000)    


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
            
         # Inyan Kara 2 added 02/21/2023   
        if 'Low Side Inyan Kara 2' not in st.session_state:
            LS_inyan_kara_2 = st.number_input('Low Side Inyan Kara 2', value = 0)    
            
        if 'Low Side Amsden' not in st.session_state:
            LS_20_high_amsden = st.number_input('Low Side Amsden', value = 0)  
        if 'Low Side Frobisher-Alida' not in st.session_state:
            LS_frobisher_alida = st.number_input('Low Side Frobisher-Alida', value = 0)  
        if 'Low Side Upper Bakken' not in st.session_state:
            LS_upper_bakken = st.number_input('Low Side Upper Bakken', value = 8400)  
            

    with col2.expander('Most Likely Pore Pressure Inputs (PSI)'):
        if 'Most Likely Inyan Kara' not in st.session_state:
            ML_inyan_kara = st.number_input('Most Likely Inyan Kara', value = 3600)
         
        
        # added 02/21/2023   
        if 'Most Likely Inyan Kara 2' not in st.session_state:
            ML_inyan_kara_2 = st.number_input('Most Likely Inyan Kara 2', value = 0)
            
            
   
            
        if 'Most Likely Amsden' not in st.session_state:
            ML_20_high_amsden = st.number_input('Most Likely Amsden', value = 0)  
        if 'Most Likely Frobisher-Alida' not in st.session_state:
            ML_frobisher_alida = st.number_input('Most Likely Frobisher-Alida', value = 0)  
        if 'Most Likely Upper Bakken' not in st.session_state:
            ML_upper_bakken = st.number_input('Most Likely Upper Bakken', value = 8850)  
            
            
    with col3.expander('High Side Pore Pressure Inputs (PSI)'):
        if 'High Side Inyan Kara' not in st.session_state:
            HS_inyan_kara = st.number_input('High Side Inyan Kara', value = 3700)
            
            # added 02/21/2023            
        if 'High Side Inyan Kara 2' not in st.session_state:
            HS_inyan_kara_2 = st.number_input('High Side Inyan Kara 2', value = 3700)
            
            
            
        if 'High Side Amsden' not in st.session_state:
            HS_20_high_amsden = st.number_input('High Side Amsden', value = 0)  
        if 'High Side Frobisher-Alida' not in st.session_state:
            HS_frobisher_alida = st.number_input('High Side Frobisher-Alida', value = 0)  
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
                  (int (inyan_kara_upload.TVD)),
                  (int(inyan_kara_upload.TVD) + 20)):
                     df_LS['LS_PSI'][i] = LS_inyan_kara

        for i in range(len(df_LS)):                
            if LS_inyan_kara == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                 (int(inyan_kara_upload.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_LS['LS_PSI'][i] =  (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1])  

                # added 02/21/2023
        for i in range(len(df_LS)):

            if LS_inyan_kara_2 == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                  (int (inyan_kara_upload_2.TVD)),
                  (int(inyan_kara_upload_2.TVD) + 20)):
                     df_LS['LS_PSI'][i] = LS_inyan_kara_2
                
        for i in range(len(df_LS)):                
            if LS_inyan_kara_2 == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                 (int(inyan_kara_upload_2.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_LS['LS_PSI'][i] =  (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1])  
                
                
                
                
                

        for i in range(len(df_LS)):
            if LS_20_high_amsden == 0:
                continue
            if df_LS['DEPTH'][i] in range(
                 (int(amsden_upload.TVD) - 20),
                 (int(amsden_upload.TVD) + 0)):
                     df_LS['LS_PSI'][i] = LS_20_high_amsden

        for i in range(len(df_LS)):            
            if LS_frobisher_alida == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(frobisher_alida_upload.TVD) - 10),
                (int(frobisher_alida_upload.TVD) + 10)):
                     df_LS['LS_PSI'][i] = LS_frobisher_alida



        for i in range(len(df_LS)):     
            if LS_frobisher_alida == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(frobisher_alida_upload.TVD) + 10),
                (int(frobisher_alida_upload.TVD) + 130)):
                    df_LS['LS_PSI'][i] = (LS_Formation_water_Density_2 * 20) + (df_LS['LS_PSI'][i-1]) 

        for i in range(len(df_LS)):            
            if LS_upper_bakken == 0:
                continue
            if round(df_LS['DEPTH'][i]) in range(
                (int(upper_bakken_upload.TVD) + 0),
                (int(upper_bakken_upload.TVD) + 160)):
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
                 (int(inyan_kara_upload.TVD)),
                 (int(inyan_kara_upload.TVD) + 20)):
                    df_ML['ML_PSI'][i] = ML_inyan_kara

        for i in range(len(df_ML)):                 
            if ML_inyan_kara == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(inyan_kara_upload.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_ML['ML_PSI'][i] =  (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])     
                
                
                
                #added 02/21/2023
        for i in range(len(df_ML)): 
            if ML_inyan_kara_2 == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(inyan_kara_upload_2.TVD)),
                 (int(inyan_kara_upload_2.TVD) + 20)):
                    df_ML['ML_PSI'][i] = ML_inyan_kara_2

        for i in range(len(df_ML)):                 
            if ML_inyan_kara_2 == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(inyan_kara_upload_2.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_ML['ML_PSI'][i] =  (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])     

                
                
                
                
                
                

        for i in range(len(df_ML)):                 
            if ML_20_high_amsden == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(amsden_upload.TVD) - 20),
                 (int(amsden_upload.TVD) + 0)):
                    df_ML['ML_PSI'][i] = ML_20_high_amsden 

        for i in range(len(df_ML)):                 
            if ML_frobisher_alida == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.TVD) - 10),
                 (int(frobisher_alida_upload.TVD + 10))):
                    df_ML['ML_PSI'][i] = ML_frobisher_alida

        for i in range(len(df_ML)):                 
            if ML_frobisher_alida == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.TVD) + 10),
                 (int(frobisher_alida_upload.TVD + 130))):
                    df_ML['ML_PSI'][i] = (ML_Formation_water_Density_2 * 20) + (df_ML['ML_PSI'][i-1])   

        for i in range(len(df_ML)):                 
            if ML_upper_bakken == 0:
                continue
            if df_ML['DEPTH'][i] in range(
                 (int(upper_bakken_upload.TVD)),
                 (int(upper_bakken_upload.TVD) + 160)):
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
                 (int(inyan_kara_upload.TVD)),
                 (int(inyan_kara_upload.TVD) + 20)):
                    df_HS['HS_PSI'][i] = HS_inyan_kara

        for i in range(len(df_HS)):                 
            if HS_inyan_kara == 0:
                    continue
            if df_HS['DEPTH'][i] in range(
                 (int(inyan_kara_upload.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_HS['HS_PSI'][i] =  (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])

                
                
                # added 02/21/2023
        for i in range(len(df_HS)): 
            if HS_inyan_kara_2 == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(inyan_kara_upload_2.TVD)),
                 (int(inyan_kara_upload_2.TVD) + 20)):
                    df_HS['HS_PSI'][i] = HS_inyan_kara_2

        for i in range(len(df_HS)):                 
            if HS_inyan_kara_2 == 0:
                    continue
            if df_HS['DEPTH'][i] in range(
                 (int(inyan_kara_upload_2.TVD) + 20),
                 (int(swift_upload.TVD))):
                    df_HS['HS_PSI'][i] =  (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])

                
                
                
        for i in range(len(df_HS)):                 
            if HS_20_high_amsden == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(amsden_upload.TVD) - 20),
                 (int(amsden_upload.TVD) + 0)):
                    df_HS['HS_PSI'][i] = HS_20_high_amsden 

        for i in range(len(df_HS)):                 
            if HS_frobisher_alida == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.TVD) - 10),
                 (int(frobisher_alida_upload.TVD + 10))):
                    df_HS['HS_PSI'][i] = HS_frobisher_alida


        for i in range(len(df_HS)): 
            if HS_frobisher_alida == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(frobisher_alida_upload.TVD) + 10),
                 (int(frobisher_alida_upload.TVD + 130))):
                    df_HS['HS_PSI'][i] = (HS_Formation_water_Density_2 * 20) + (df_HS['HS_PSI'][i-1])

        for i in range(len(df_HS)):             
            if HS_upper_bakken == 0:
                continue
            if df_HS['DEPTH'][i] in range(
                 (int(upper_bakken_upload.TVD)),
                 (int(upper_bakken_upload.TVD) + 160)):
                    df_HS['HS_PSI'][i] = HS_upper_bakken      

                
                
# Create a function to iterate a loop to add Lithology, Ts, and Ko to the OVBD log

    
    def FG_calcs():
        
        for i in range(len(df_ovbd)):
            depth_value = df_ovbd['DEPTH'][i]

            for index, row in enumerate(merge_df.values):
                try:
                    if (depth_value >= merge_df.iloc[index, 1]) & (depth_value <= merge_df.iloc[index + 1, 1]):
   
                        
                        df_ovbd['Ko'][i] = float(merge_df.iloc[index, 3])
                        #st.write(df_ovbd)
                        df_ovbd['Ts'][i] = float(merge_df.iloc[index, 4])

                except:
                    if depth_value > merge_df['TVD'].iloc[index - 1]:
                        df_ovbd['Ko'][i] = float(merge_df.iloc[index, 3])
                        df_ovbd['Ts'][i] = float(merge_df.iloc[index, 4])
                        
                        
                

    # This works and is current!    
    pierre_upload = new_df[new_df['TopName'] == 'PIERRE']
    greenhorn_upload = new_df[new_df['TopName'] == 'GREENHORN']
    belle_fourche_upload = new_df[new_df['TopName'] == 'BELLE_FOURCHE']
    mowry_upload = new_df[new_df['TopName'] == 'MOWRY']
    inyan_kara_upload = new_df[new_df['TopName'] == 'INYAN_KARA']
    inyan_kara_upload_2 = new_df[new_df['TopName'] == 'INYAN_KARA_2']
    swift_upload = new_df[new_df['TopName'] == 'SWIFT']
    rierdon_upload = new_df[new_df['TopName'] == 'RIERDON']
    amsden_upload = new_df[new_df['TopName'] == 'AMSDEN']
    tyler_upload = new_df[new_df['TopName'] == 'TYLER']
    kibbey_lime_upload = new_df[new_df['TopName'] == 'KIBBEY_LIME']
    charles_upload = new_df[new_df['TopName'] == 'CHARLES']
    top_last_salt_upload = new_df[new_df['TopName'] == 'TOP_LAST_SALT']
    base_last_salt_upload = new_df[new_df['TopName'] == 'BASE_LAST_SALT']
    frobisher_alida_upload = new_df[new_df['TopName'] == 'FROBISHER-ALIDA_INTERVAL']
    lodgepole_upload = new_df[new_df['TopName'] == 'LODGEPOLE']
    upper_bakken_upload = new_df[new_df['TopName'] == 'UPPER_BAKKEN_SHALE']
    middle_bakken_upload = new_df[new_df['TopName'] == 'MIDDLE_BAKKEN']
    lower_bakken_upload = new_df[new_df['TopName'] == 'LOWER_BAKKEN_SHALE']
    three_forks_upload = new_df[new_df['TopName'] == 'THREE_FORKS']
    birdbear_upload = new_df[new_df['TopName'] == 'BIRDBEAR']  
    

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

    
    def convert_df(df_ovbd):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df_ovbd.to_csv().encode('utf-8')
    st.download_button(
     label = "Download data as CSV",
     data = convert_df(df_ovbd),
     file_name = 'Overburden_Dataframe.csv',
     mime = 'csv'
 ) 
    
    plot = go.Figure()
    plot.add_trace(go.Scatter( x = df_ovbd["OVBD_PPG"], y = df_ovbd["DEPTH"], name = 'Overburden'))
    plot.add_trace(go.Scatter(x = df_LS['LS_PPG'], y = df_LS['DEPTH'], line_dash = 'dot', name = 'LS Pore Pressure', marker_color ="#4169E1"))
    plot.add_trace(go.Scatter(x = df_ML['ML_PPG'], y = df_ML['DEPTH'], line_dash = 'dot', name = 'ML Pore Pressure', marker_color ="#00C957"))
    plot.add_trace(go.Scatter(x = df_HS['HS_PPG'], y = df_HS['DEPTH'], line_dash = 'dot', name = 'HS Pore Pressure', marker_color ="#FF4040"))
    plot.add_trace(go.Scatter(x = df_ovbd['LS_FG_PPG'], y = df_ovbd['DEPTH'], name = 'LS Frac Gradient', marker_color ="#4169E1"))
    plot.add_trace(go.Scatter(x = df_ovbd['ML_FG_PPG'], y = df_ovbd['DEPTH'], name = 'ML Frac Gradient', marker_color ="#00C957"))
    plot.add_trace(go.Scatter(x = df_ovbd['HS_FG_PPG'], y = df_ovbd['DEPTH'], name = 'HS Frac Gradient', marker_color ="#FF4040"))
    
    
    plot.update_yaxes(nticks = 30, range = [max(new_df['TVD']) + 500, 0]) #, autorange = 'reversed')
    plot.update_xaxes(nticks = 40, showgrid=True, gridcolor = 'lightgray')
    
    title_input = st.sidebar.text_input('Enter Well Name' ,'Well Name')
    plot.update_layout(title_text = (title_input  + '<br>    Pore Pressure Log Plot'), 
                       title_x = .3, 
                       xaxis_title="PPG",
                       yaxis_title="TVD",
                       height = 1200,
                       width = 800,
                       template='plotly')
    def Topnames():
            for row in merge_df.iterrows():
                if row[1]['Plot?'] is not '':
            

                    plot.add_hline(y = row[1]['TVD'],
                                   line_dash = 'dot',
                                   annotation_text = row[1]['TopName'],
                                  annotation_position = 'top left') 
    Topnames()
    
    
    
#     plot.add_hline(y = int(pierre_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Pierre', annotation_position = 'top left')
#     plot.add_hline(y = int(greenhorn_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Greenhorn', annotation_position = 'top left')
#     plot.add_hline(y = int(greenhorn_upload['TVD']) + 200, line_dash="dot", row=1, col="all", annotation_text = 'Greenhorn Silt', annotation_position = 'top left')
#     plot.add_hline(y = int(mowry_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Mowry', annotation_position = 'top left')
#     plot.add_hline(y = int(inyan_kara_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Inyan Kara', annotation_position = 'top left')
#     plot.add_hline(y = int(swift_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Swift', annotation_position = 'top left')
#     plot.add_hline(y = int(rierdon_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Rierdon', annotation_position = 'top left')
#     plot.add_hline(y = int(amsden_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Amsden', annotation_position = 'top left')
#     plot.add_hline(y = int(tyler_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Tyler', annotation_position = 'top left')
#     plot.add_hline(y = int(kibbey_lime_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Kibbey Lime', annotation_position = 'top left')
#     plot.add_hline(y = int(charles_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Charles', annotation_position = 'top left')
#  #   plot.add_hline(y = int(top_last_salt_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Top Last Salt', annotation_position = 'top left')
#  #   plot.add_hline(y = int(base_last_salt_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Base Last Salt', annotation_position = 'top left')
#     plot.add_hline(y = int(frobisher_alida_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Frobisher Alida', annotation_position = 'top left')
#     plot.add_hline(y = int(upper_bakken_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Upper Bakken Shale', annotation_position = 'top left')
#  #   plot.add_hline(y = int(lower_bakken_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Lower Bakken Shale', annotation_position = 'top left')
#     plot.add_hline(y = int(birdbear_upload['TVD']), line_dash="dot", row=1, col="all", annotation_text = 'Birdbear', annotation_position = 'top left')

    st.plotly_chart(plot, use_container_width=True)

    convert_df(df_ovbd)


    
    
def data_summary():
    st.header('Statistics of Dataframe')
    st.write(df_ovbd.describe())



home()
if options == 'Yes':
    calc()
else:
  ''
#added 02/21/2023
if options_2 == 'Yes':
    troubleshooting()
else:
    ''  
    
interactive_plot()
data_summary()
