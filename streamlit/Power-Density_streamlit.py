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


st.title('Power Density')
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

# Example of how to do a plotly plot
# #Plotly test, throw this away for something better later.
# expl_dict = {'Prob':['Ptemp','Pperm','Pchem'], 'Values':[Ptemp, Pperm, Pchem]}
# exploration_df = pd.DataFrame(data=expl_dict)

# fig = px.bar(data_frame = exploration_df, y='Prob', x='Values', orientation='h', range_x=[0,1])
# st.plotly_chart(fig)



##Appraisal and dev inputs###################
st.markdown("___")
st.write("## Appraisal and Dev Parameters")

colA, colB = st.beta_columns(2) # Show sliders in 2 columns

#probably should add a message/try catch that this must be numeric:
Tmax = float(colA.text_input("Startup averages temperature for P90 reserves (degrees C)", 280))
Tmin = float(colB.text_input("Minimum temperature for the P10 reservoir (degrees C)", 250))

# USER INPUT REQUIRED
# Area > 250 deg C in km2

#st.markdown("**Area > 250 degrees C, in KM^2**")
Area_P90 = float(colA.text_input("Area > 250 degrees C, in KM^2 P90:", 1))
Area_P10 = float(colB.text_input("Area P10:", 10))

# USER INPUT REQUIRED
#st.write("**Power Density 250 to 280 deg C (MWe/km2)**")
PowerDens_P90 = float(colA.text_input("Power density in (MWe/km2) P90:", 10))
PowerDens_P10 = float(colB.text_input("Power Density P10:", 24))


## CALCULATIONS ################################################
# Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)
area_nu = ((np.log(Area_P90)+np.log(Area_P10))/2)


area_sigma = (np.log(Area_P10)-np.log(Area_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

powerdens_nu = ((np.log(PowerDens_P90)+np.log(PowerDens_P10))/2)


powerdens_sigma = (np.log(PowerDens_P10)-np.log(PowerDens_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))


# Calculate nu and sigma for MWe Capacity
capacity_nu = area_nu + powerdens_nu


capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5

prob_df = calculate_cumulative_conf(Area_P90, Area_P10, PowerDens_P90, PowerDens_P10)

fig = px.bar(data_frame = prob_df, y='Cumulative confidence (%)', x='expected development size (MW)', orientation='h', range_x=[0,500])
st.plotly_chart(fig)

# Line plot
#fig = px.line(df2, x="Date", y="Cases")
#st.plotly_chart(fig)
#fig = px.bar(data_frame = prob_df, y='Prob', x='expected development size (MW)', orientation='h', range_x=[0,500])
#st.plotly_chart(fig)

### Text output ###
st.markdown("___")
st.write("## Outputs")
st.write("Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)", area_nu)
st.write("Area sigma", area_sigma)
# Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)
st.write("Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)")
st.write("Power density nu ",powerdens_nu)
st.write("Power density sigma ", powerdens_sigma)
"capacity_sigma", capacity_sigma
"capacity_nu", capacity_nu

st.markdown("___")
st.write("## Download your confidence curve:")

if st.button('Build CSV for download'):
    tmp_download_link = download_link(prob_df, 'YOUR_DF.csv', 'CSV built! Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)


##### FINAL PLOTS ######################
# Plot power capacity cumulative distribution
##### better to change it to streamlit native plots I think for interactivity (hover and see value)
##### I've just ported over the notebook code for a quick placeholder
#colA, colB = st.beta_columns(2) # Show sliders in 2 columns
#figPowerCapacity = plt.figure()
#plt.plot(expected_power_capacity, prob_desc)
#plt.xlabel("Expected Power Capacity (MWe potential reserves)")
#plt.ylabel("Cumulative Confidence %")
#plt.title("Cumulative Confidence in Power Capacity")
#colA.pyplot(fig=figPowerCapacity)
#
#
## Plot expected development size cumulative distribution
#figDevSize = plt.figure()
#plt.plot(expected_development_size, prob_desc)
#plt.xlabel("Expected Development Size (MW)")
#plt.ylabel("Cumulative Confidence %")
#plt.title("Cumulative Confidence in Developed Reservoir Size")
#colB.pyplot(fig=figDevSize)



