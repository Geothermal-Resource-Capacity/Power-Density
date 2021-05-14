# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:31:30 2021

"""
# Import libraries for viz
import streamlit as st
import plotly.express as px
import pandas as pd
import base64

#libs for computation
import numpy as np
import scipy
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt

def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download. from https://discuss.streamlit.io/t/heres-a-download-function-that-works-for-dataframes-and-txt/4052

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


def calculate_cumulative_conf(areaP90: float=1., areaP10: float=10., pdP90: float=10., pdP10: float=24):
    """Calculate cumulative confidence level for expected development size in MW

    Args:
        areaP90 (float): pessimistic area in sqkm
        areaP10 (float): optimistic area in sqkm
        pdP90 (float): pessimistic power density in MWe/sqkm
        pdP10 (float): optimistic power density in MWe/sqkm

    Returns:
        prob_df (pandas Dataframe): cumulative confidence curve in Reservoir Size
    """
    # calculate area > 250 °C
    area_mu = ((np.log(areaP90)+np.log(areaP10))/2)
    area_sigma = (np.log(areaP10)-np.log(areaP90))/((norm.ppf(0.9)-(norm.ppf(0.1))))

    # calculate powerdensity mean and standard dev
    powerdens_mu = ((np.log(pdP90)+np.log(pdP10))/2)
    powerdens_sigma = (np.log(pdP10)-np.log(pdP90))/((norm.ppf(0.9)-(norm.ppf(0.1))))


    capacity_mu = area_mu + powerdens_mu
    capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5
    eds = [lognorm.ppf(x/100, capacity_sigma, loc=0, scale=np.exp(capacity_mu)) for x in range(0,100)]
    indx = list(np.arange(0,100)[::-1])
    edsepc_tups = list(zip(indx,eds))
    prob_df = pd.DataFrame(edsepc_tups, columns = ['Cumulative confidence (%)', 'expected development size (MW)'])

    return prob_df



###########################################################################
## END of functions - Streamlit app below #################################
###########################################################################

st.title('Power Density')
st.write("Evaluation of geothermal resources")

#Post figure image at the top
###Future goal - make this interactive, see points on hover and show current analysis as a point
imgPath = 'https://github.com/Geothermal-Resource-Capacity/Power-Density/blob/main/figures/wilmarth_2019.PNG'
#This built in function is breaking, so I'm trying another method
#st.image(imgPath, caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
#Alternate method for displaying image:
#  From: https://pmbaumgartner.github.io/streamlitopedia/sizing-and-images.html
# This will eventually be replaced by a interactive graph, so not a big deal.
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("imgPath")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)
### End of image (figure) ########

st.write('**1: Exploration, is it there?**') #Streamlit uses markdown for formatting

# Exploration portion of inputs ##########################
col1, col2, col3 = st.beta_columns(3) # Show sliders in 3 columns

st.write("## Exploration Parameters")
Ptemp = col1.slider('PTemperature', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Ptemp')
Pperm = col2.slider('PPermeability', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Pperm')
Pchem = col3.slider('Pchemistry', value=95, min_value=1, max_value=100,step=1, format='%i%%', key='Pchem')
Ptemp /= 100 #Keep things in decimal percent, but display in percent. st isn't good about formating yet
Pperm /= 100 #  These don't need to be in the sidebar, but I want them close to the input
Pchem /= 100 #  I think it makes things clearer.

#Show exploration input results ###################################
POSexpl = Ptemp * Pperm * Pchem
#print("Probability of exploration success = {:.2f}%".format(round(POSexpl*100,0)))
# Could potentially code in user option to adjust number of decimal places for POS

st.write(f'{Ptemp} \* {Pperm} * {Pchem} = Probability of exploration success {round(POSexpl*100,1)}%')

##Appraisal and dev inputs###################
st.markdown("___")
st.write("## Appraisal and Dev Parameters")

colA, colB = st.beta_columns(2) # Show sliders in 2 columns

#probably should add a message/try catch that this must be numeric:
Tmax = float(colA.text_input("Startup averages temperature for P90 reserves (degrees C)", 280))
Tmin = float(colB.text_input("Minimum temperature for the P10 reservoir (degrees C)", 250))

# USER INPUT 
# Area > 250 deg C in km2

#st.markdown("**Area > 250 degrees C, in KM^2**")
Area_P90 = float(colA.text_input("Area > 250 degrees C, in KM^2 P90:", 1))
Area_P10 = float(colB.text_input("Area P10:", 10))

# USER INPUT 
#st.write("**Power Density 250 to 280 deg C (MWe/km2)**")
PowerDens_P90 = float(colA.text_input("Power density in (MWe/km2) P90:", 10))
PowerDens_P10 = float(colB.text_input("Power Density P10:", 24))


## CALCULATIONS ################################################
# Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)
area_nu = ((np.log(Area_P90)+np.log(Area_P10))/2)
area_sigma = (np.log(Area_P10)-np.log(Area_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for the power density
powerdens_nu = ((np.log(PowerDens_P90)+np.log(PowerDens_P10))/2)
powerdens_sigma = (np.log(PowerDens_P10)-np.log(PowerDens_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for MWe Capacity
capacity_nu = area_nu + powerdens_nu
capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5

# Calculate cumulative confidence curve
prob_df = calculate_cumulative_conf(Area_P90, Area_P10, PowerDens_P90, PowerDens_P10)

fig = px.bar(data_frame = prob_df, y='Cumulative confidence (%)', x='expected development size (MW)', orientation='h', range_x=[0,500])
st.plotly_chart(fig)

st_ex_AdvancedOutput = st.beta_expander(label="Computation outputs") #Make an expander object
with st_ex_AdvancedOutput:   #Make these results hidden until expanded
    ### Text output ###
    st.markdown("___")
    #st.write("## Computation outputs ")
    #Display the table, only every 10th row, and hide the index column to make it pretty
    st.table(prob_df[prob_df.index%10==9].assign(hideIndex='').set_index('hideIndex'))

    st.write("Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)", area_nu)
    st.write("Area sigma", area_sigma)
    # Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)
    st.write("Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)")
    st.write("Power density nu ",powerdens_nu)
    st.write("Power density sigma ", powerdens_sigma)
    "capacity_sigma", capacity_sigma
    "capacity_nu", capacity_nu

    st.markdown("___")

#Perhaps this should be in the 'advanced' view expander too
st.write("### Download confidence curve values:")

if st.button('Build CSV for download'):
    tmp_download_link = download_link(prob_df, 'cum_conf_curve.csv', 'CSV built! Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

st.write("") #blank line so space it out
st.write("Made with ❤️ at [SWUNG 2021 geothermal hack-a-thon](https://softwareunderground.org/events/2021/5/13/geothermal-hackathon)")
st.write("[github repo](https://github.com/Geothermal-Resource-Capacity) includes contact info.")