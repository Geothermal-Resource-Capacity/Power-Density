# -*- coding: utf-8 -*-
"""
App created on Thu May 13 09:31:30 2021
Then expanded on with love. 

This app remains a work in progress :-) 

Key changes needed include:
-   Chat to Jan about the addion of mean and sd of input paramaters. 
    Perhaps it would be better to include an option to download the paramaters as passed in
    plus a calculated P50. It would also be useful to include the P10-P50-P90 MWe result in this. 

-   Copy edit and trim the text. 

-   Remake the power density plot into something that better reflects the underlying data.

-   Set up to call the calculate_cumulative_conf from a helper function file 
    rather than repeat here and elsewhere in the repo. 

There are a number of working refinements and thoughts throughout this file tagged with "NOTE"

"""

# Import libraries for viz
import streamlit as st
import plotly.express as px
import pandas as pd
import base64
from pathlib import Path

# Import libraries for computation
import numpy as np
import scipy
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt

# ================
# Helper functions
# ================

# NOTE We should look at calling the calculate_cumulative_conf function from a centralized function file

def download_link(object_to_download, download_filename, download_link_text):
    """Generates a link from which the user can download object_to_download 
    
    Method from https://discuss.streamlit.io/t/heres-a-download-function-that-works-for-dataframes-and-txt/4052

    Args:   object_to_download (str, pd.DataFrame):  The object to be downloaded
            download_filename (str): Filename and extension of file (e.g. mydata.csv or some_txt_output.txt)
            download_link_text (str): Text to display for download link

    Example:   download_link(YOUR_DF, 'YOUR_DF.csv', 'CSV built! Click here to download your data!')
    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=True)

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


# =============
# Streamlit app
# =============


# ----------------------
# Headder and intro text
# ----------------------

st.title('Exploration Tool for Conventional Geothermal Resources')

st.write('This tool supports the process used by a technical resource team to ' + 
    '(1) estimate the probability of exploration success and (2) make a ' + 
    'probabilistic estimate of resource capacity using the lognormal power density method.')

st.markdown("___")

# -----------------------------------
# Estimate the probability of success 
# -----------------------------------


#
# Intro text 
#

st.write('## 1: Is it there?')

st.write('Estimate the probability of exploration success')

# NOTE need to find better way of formatting lists

st.write('Based on the data available, what is you percent confidence that the prospect has:') 
st.write('1. Sufficient temperature for the desired power conversion technology or direct use application')
st.write('2. Enough permeability to support economic well flows')
st.write('3. Benign or manageable fluid chemistry') 

st.write(' ') # NOTE need to look into better method for spacing layout 


#
# Make sliders
#

col1, col2, col3 = st.beta_columns(3) # Show sliders in 3 columns

Ptemp = col1.slider('Temperature', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Ptemp')
Pperm = col2.slider('Permeability', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Pperm')
Pchem = col3.slider('Chemistry', value=95, min_value=1, max_value=100,step=1, format='%i%%', key='Pchem')


#
# Calculate POS in decimal percent
#

Ptemp /= 100 
Pperm /= 100
Pchem /= 100

POSexpl = Ptemp * Pperm * Pchem


#
# Output POS result to app in percent rounded to nearest whole number
#

st.write(f'{round(Ptemp*100)}% temperature \* {round(Pperm*100)}% permeability ' +
    f'* {round(Pchem*100)}% chemistry = {round(POSexpl*100)}% probability of exploration success')


#
# App formatting
#

st.markdown("___")


# -----------------------
# Estimate power capacity
# -----------------------


#
# Intro text
#

st.write("## 2: How big is it?")

st.write('Power density is one of several methods used to evaluate the ' + 
    'development capacity of conventional geothermal resources. It involves ' +
    'multiplying the likely area of the productive resource (km2) with a ' + 
    'power density (MWe/km2), where the former is defined using a ' + 
    'conceptual model and the latter by comparison to analogous developed resources.')

st.write('The method here uses a probabilistic framework that includes ' + 
    'pessimistic (P90), most likely (P50) and optimistic (P10) estimates of ' +
    'area and power density and subsequently returns a probabilistic power capacity estimate.')


#
# Areas from the concept model (image and text)
#

st.write('### P90, P10 Conceptual Model Example')

st.write('Resource data are integrated into a conceptual model, which is ' + 
    'a systematic description of where fluid may flow though the crust and ' + 
    'what the temperature, phase and chemistry of the fluid may be. ' + 
    'The area estimates projected to surface for the P10 and P90 include only ' + 
    'the potentially productive resource. The potentially productive resource depends on' + 
    'the desired power conversion technology or direct use application. Figure from Cumming 2016')

imgPath1 = 'https://github.com/Geothermal-Resource-Capacity/Power-Density/blob/improve_streamlit_markdown/figures/Cumming_2016_ConceptModel.png?raw=true'
st.image(
    image=imgPath1, 
    caption=None, 
    width=None, 
    use_column_width=None, 
    clamp=False, 
    channels='RGB', 
    output_format='auto')


#
# Power density from analogues (image and text)
#

st.write('### Global Power Density')

st.write('The plot below depicts power density calculated by dividing the ' + 
    'sustained production in MWe by the area within a merged 500 m buffer ' + 
    'placed around production wells. A power density for the exploration prospect ' + 
    'prior to drilling is selected based on similarity in the geologic setting and ' + 
    'temperature. As more data becomes available for an exploration prospect, ' + 
    'specific power density analogues may be identified. Figure from Wilmarth et al. 2015.')

imgPath2 = 'https://github.com/Geothermal-Resource-Capacity/Power-Density/blob/main/figures/wilmarth_2019.PNG?raw=true'
st.image(
    image=imgPath2, 
    caption=None, 
    width=None, 
    use_column_width=None, 
    clamp=False, 
    channels='RGB', 
    output_format='auto')

# NOTE Would be good to make the power density plot interactive in future
# NOTE Would be good to have another version of the power density plot that makes the underlying data clearer
# NOTE Perhaps include something like toggling over datapoints to see the field name?


#
# Pass in user paramaters for power density estimate
#

st.write('### Input Paramaters')
st.write('Input your P90 (pessimistic) and P10 (optimistic) estimates for ' + 
    'temperature, area and power density to output lognormal power capacity (MW) and P50 area')

colA, colB = st.beta_columns(2) # Show input cells in 2 columns

# NOTE should probably should add a message/try catch that says these fields must be numeric
Tmax = float(colA.text_input("Average temperature (degC) in the P90 area", 280))
Tmin = float(colB.text_input("Minimum temperature for the P10 area (degC)", 250))

Area_P90 = float(colA.text_input("P90 (pessimistic) production area (km2)", 1))
Area_P10 = float(colB.text_input("P10 (optimistic) production area (km2)", 10))

PowerDens_P90 = float(colA.text_input("P90 (pessimistic) power density (MWe/km2)", 10))
PowerDens_P10 = float(colB.text_input("P10 (optimistic) power density (MWe/km2)", 24))

#
# Power density calculations (under the hood)
#

# Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)
area_nu = ((np.log(Area_P90)+np.log(Area_P10))/2)
area_sigma = (np.log(Area_P10)-np.log(Area_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for the power density
powerdens_nu = ((np.log(PowerDens_P90)+np.log(PowerDens_P10))/2)
powerdens_sigma = (np.log(PowerDens_P10)-np.log(PowerDens_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for MWe Capacity
capacity_nu = area_nu + powerdens_nu
capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5

indices = ['area [sqkm]', 'power_density [MWe/sqkm]', 'capacity [MWe]']
means_std = {'mean': [area_nu, powerdens_nu, capacity_nu],
            'stdev': [area_sigma, powerdens_sigma, capacity_sigma]}

param_df = pd.DataFrame.from_dict(means_std, orient='index', columns=indices)

# Calculate cumulative confidence curve
prob_df = calculate_cumulative_conf(Area_P90, Area_P10, PowerDens_P90, PowerDens_P10)


#
# Output to user the lognormal P50 area
#

st.write('need to output the P50 area here')


#
# Output to user the power capacity results
#

st.write('### Output Power Capacity')

# Print simple results summary

st.write('TBC - format the P10, P50 and P90 MWe output here as f string')

# Plot cumulative confidence curve

fig = px.bar(
    data_frame = prob_df, 
    y='Cumulative confidence (%)', 
    x='expected development size (MW)', 
    orientation='h', 
    range_x=[0,500])

st.plotly_chart(fig)

# Show/hide full results summary

st_ex_AdvancedOutput = st.beta_expander(label="Detailed output") # Make an expander object

with st_ex_AdvancedOutput:   # Make these results hidden until expanded
    ### Text output ###
    st.markdown("___")
    #st.write("## Computation outputs ")
    # Display the table, only every 10th row, and hide the index column to make it pretty
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


#
# Results download for user
#

# NOTE perhaps include the download options in the 'advanced' view expander view

st.write("### Download confidence curve values:")

if st.button('Build Confidence-curve CSV for download'):
    tmp_download_link = download_link(prob_df, 'cum_conf_curve.csv', 'CSV built! Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)

if st.button('Build parameter CSV for download'):
    tmp_download_link_params = download_link(param_df, 'parameter_values.csv', 'CSV built! Click here to download your data!')
    st.markdown(tmp_download_link_params, unsafe_allow_html=True)

st.write("") # blank line so space it out
st.write("Made with ❤️ at [SWUNG 2021 geothermal hack-a-thon](https://softwareunderground.org/events/2021/5/13/geothermal-hackathon)")
st.write("[github repo](https://github.com/Geothermal-Resource-Capacity) includes contact info.")