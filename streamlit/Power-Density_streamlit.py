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
    prob_df = pd.DataFrame(edsepc_tups, columns = ['Cumulative confidence (%)', 'Expected development size (MWe)'])

    return prob_df


# =============
# Streamlit app
# =============

# ----------------------
# Headder and intro text
# ----------------------

st.title('Conventional Geothermal Resource Exploration Tool')

st.write('This tool does the calculations required for estimating the:')

st.write('1. Probability of exploration success') 
st.write('2. Resource capacity using a probabilistic, lognormal power density method')

st.markdown("___")

# -----------------------------------
# Estimate the probability of success 
# -----------------------------------

st.write('# 1. Probability of Exploration Success')

st.write('This is a transparent method for estimating the probability of exploration success, ' + 
    'where exploration success is defined as discovering a commercially viable resource.')

# NOTE need to find better way of formatting lists

st.write('Estimate the percent confidence that the prospect has the following ' + 
    'based on the available resource data and the conceptual model:') 

st.write('1. Sufficient temperature for the desired power conversion technology or direct use application')
st.write('2. Enough permeability to support economic well flows (self-flowing or pumped wells)')
st.write('3. Benign or manageable fluid chemistry') 

st.write(' ') # NOTE need to look into better method for spacing layout 

#
# Make sliders
#

col1, col2, col3 = st.columns(3) # Show sliders in 3 columns

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

st.write(f'_{round(Ptemp*100)}% temperature \* {round(Pperm*100)}% permeability ' +
    f'* {round(Pchem*100)}% chemistry = {round(POSexpl*100)}% probability of exploration success_')


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

st.write("# 2. Power Capacity")

st.write('Power density is one of several methods used to evaluate the ' + 
    'power capacity of conventional geothermal resources. ' + 
    'The power density method implemented here uses a probabilistic framework where ' + 
    'pessimistic (P90) and optimistic (P10) estimates of area and power density ' +
    'are input and a probability distribution of power capacity is returned. ' +
    'The entire method involves three steps, and this tool does the calculations required for the third step.')

st.write('**Step 1:** Integrates available resource data into a set of conceptual models ' +
    'that reflect the smallest (pessimistic, P90) and largest (optimistic, P10) resource ' +
    'that could be present. The P50 model is typically also discussed at this stage, but is not an input parameter for Step 3. ' + 
    'Refer to [Cumming 2009](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2009/cumming.pdf) ' +
    'for how to construct conceptual models from surface exploration data. Refer to ' +
    '[Wallis et al 2017](https://www.geothermal-energy.org/pdf/IGAstandard/NZGW/2017/111_Wallis-Final_.pdf) ' + 
    'for approaches to reservoir volume uncertainty and a tool that assists with developing the P10/P90 end-member models.')

st.write('**Step 2:** Project the potentially productive resource volume in the P10 and P90 conceptual models ' + 
    'to a plan-view map and calculate the area. The potentially productive resource is the extent of ' + 
    'the reservoir with sufficient temperature to support the desired power conversion technology or direct use application. ' +
    'This means that resource areas below the temperature limit of preferred power conversion technology are excluded. '
    'Refer to [Cumming 2016a](https://publications.mygeoenergynow.org/grc/1032377.pdf) (Figure 9) for ' + 
    'how to project the conceptual models to surface and calculate the area.' )

st.write('**Step 3:** Calculate the power capacity by ' +
    'multiplying the P10 and P90 area of the potentially productive resource (km2) with a range of ' + 
    'power density (MWe/km2), where the latter by comparison to analogous developed resources. ' +
    'Sections 2.1 and 2.2 below are designed to assist resource scientists with this step. '
    'The lognormal approach to power density used in this web-app is described in ' +
    '[Cumming 2016b](https://pangea.stanford.edu/ERE/pdf/IGAstandard/SGW/2016/Cumming.pdf).')

# --------------------------------
# Select Appropriate Power Density
# --------------------------------

st.write('# 2.1 Estimate Power Density')

st.write('Power density is defined as the sustainable generation (in megawatts) per square kilometer of productive resource area. '+
    'Below we step through how a reasonable range of power capacity can be identified for an exploration prospect. ')

st.write('Temperature has a great influence on power capacity, so we first use the conceptual model to constrain likely resource temperature.')

colA, colB = st.columns(2)

# NOTE should probably should add a message/try catch that says these fields must be numeric
Tmax = float(colA.text_input("Average temperature (degC) in the P90 area", 280))
Tmin = float(colB.text_input("Minimum temperature for the P10 area (degC)", 250))

st.write('_Note that temperature values input here are used for reporting purposes and are not used in the power capacity calculation_')

st.write('Use these temperatures and the geologic setting of your prospect to ' + 
    'identify developed geothermal systems that have similar characteristics. ' +
    'We use geologic setting to identify analogues because geology influences permeability, ' + 
    'which is another resource characteristic that greatly influences power capacity. ' )

st.write('Evaluation of the production area and power capacity of well-selected developed analogues ' + 
    'provides the most reliable range of power density. ' + 
    'For open access information on developed resources, refer to conference paper databases ' +
    'maintained by the [International Geothermal Association](https://www.geothermal-energy.org/explore/our-databases/conference-paper-database/) ' + 
    'and [Geothermal Rising](https://www.geothermal-library.org/). ' + 
    'NREL maintains [geothermal wiki](https://openei.org/wiki/Geothermal_Areas) that is a growing repository of case study information.')

st.write('If no analogues can be identified, then take the minimum temperature of the P10 area ' +
    'and find a range using the database of power density that is plotted below. ' + 
    'For example, a minimum P10 temperature of 250degC would yield a power density range of 2 - 23 MW/km2.')

pd_database = pd.read_csv(r'../data/PowerDensityDatabase_Expanded.csv')
fig = px.scatter(
    pd_database, 
    x='Average temperature [degC]', 
    y='Power density [MWe/km2]', 
    color='System type',
    hover_data=['Field', 'System type', 'Average temperature [degC]', 'Enthalpy classification', 'Power density [MWe/km2]'],
)

st.plotly_chart(fig)

st.write('Power density is plotted above for developed reservoirs. It was ' + 
    'calculated by dividing the sustained production in MWe by the area within a merged 500 m buffer ' + 
    'placed around production wells. Therefore, values may not equate directly to the area of potentially productive resource ' + 
    'that is defined using the concept model process. However, it is a systematic approach and a reasonable approximation. '
    'The power density and average temperature are from Wilmarth et al. (2019), which expands on earlier work published ' + 
    '[here](https://www.geothermal-energy.org/pdf/IGAstandard/WGC/2015/16020.pdf). The system type and enthalpy classification ' +
    'are from literature review conducted by Irene Wallis. The data in this plot has been ' + 
    'made open access in [this repository](https://github.com/Geothermal-Resource-Capacity/Power-Density) under an Apache 2 license.') 

# ---------------------------
# Power capacity - user input
# ---------------------------

st.write('# 2.2 Calculate Power Capacity')
st.write('Input your P90 (pessimistic) and P10 (optimistic) estimates for ' + 
    'area from your conceptual model and power density based on developed analogues.') 

colA, colB = st.columns(2)

colA.header("Input Area")
colB.header("Input Power Density")

Area_P90 = float(colA.text_input("P90 (pessimistic) production area (km2)", 1))
PowerDens_P90 = float(colB.text_input("P90 (pessimistic) power density (MWe/km2)", 10))

Area_P10 = float(colA.text_input("P10 (optimistic) production area (km2)", 10))
PowerDens_P10 = float(colB.text_input("P10 (optimistic) power density (MWe/km2)", 24))

# ----------------------------------------------
# Power capacity - calculations (under the hood)
# ----------------------------------------------

# Calculate nu and sigma for resource area 
# (the mean and variance in log units required for specifying lognormal distributions)
area_nu = ((np.log(Area_P90)+np.log(Area_P10))/2)
area_sigma = (np.log(Area_P10)-np.log(Area_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for the power density
powerdens_nu = ((np.log(PowerDens_P90)+np.log(PowerDens_P10))/2)
powerdens_sigma = (np.log(PowerDens_P10)-np.log(PowerDens_P90))/((norm.ppf(1-0.1)-(norm.ppf(0.1))))

# Calculate nu and sigma for MWe Capacity
capacity_nu = area_nu + powerdens_nu
capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5

indices = ['area [sqkm]', 'power_density [MWe/sqkm]', 'capacity [MWe]']
p_values = {'P90': [Area_P90, PowerDens_P90, 'P90_capacity'],
            'P50': [round(np.exp(area_nu)), round(np.exp(powerdens_nu)), round(np.exp(capacity_nu))],
            'P10': [Area_P10, PowerDens_P10, 'P10_capacity']}

# NOTE double check these outputs against the cumulative confidence curve
# Why does np.exp(capacity_nu) = 49% in the cumulative confidence curve data rather than 50%?
# Would be good also to include the P90 and P10 capacity into the output table

param_df = pd.DataFrame.from_dict(p_values, orient='index', columns=indices)

# Calculate cumulative confidence curve
prob_df = calculate_cumulative_conf(Area_P90, Area_P10, PowerDens_P90, PowerDens_P10)


# ------------------------------------------
# Power capacity - simple web output to user 
# ------------------------------------------

#
# Table summarising input and output 
#

col1, col2, col3, col4 = st.columns([2,1,1,1])

# Table headder
col1.header("Output")
col2.header("P90")
col3.header("P50")
col4.header("P10")

# Row 1 - Range of areas
col1.write('Area (km2)')
col2.write(Area_P90)
col3.write(round(np.exp(area_nu),1))
col4.write(Area_P10)

# Row 2 - Range of power density
col1.write('Power Density (MWe/km2)')
col2.write(PowerDens_P90)
col3.write(round(np.exp(powerdens_nu),1))
col4.write(PowerDens_P10)

# Row 3 - Range of power capacity
col1.write('Power Capacity (MWe)')

P90_MWe = prob_df.iloc[9,1]
col2.write(round(P90_MWe,1))

P50_MWe = prob_df.iloc[49,1]
col3.write(round(P50_MWe,1))

P10_MWe = prob_df.iloc[89,1]
col4.write(round(P10_MWe,1))

#
# Plot cumulative confidence curve
#
st.write('')

# User input field for x axis max limit
cola, colb = st.columns(2)
x_max = float(cola.text_input("Maximum MWe for the cumulative confidence plot below", 500))

# Plotly plot setup
fig = px.bar(
    data_frame = prob_df, 
    y='Cumulative confidence (%)', 
    x='Expected development size (MWe)', 
    orientation='h', 
    range_x=[0,x_max])

st.plotly_chart(fig)

# -------------------------------------------------------------------------
# Power capacity - Show/hide full results summary and downloadable results 
# -------------------------------------------------------------------------

st_ex_AdvancedOutput = st.expander(label="Detailed output and downloads") # Make an expander object

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

    st.write("### Click to download results")

    # Note, new versions of streamlit have a built in download button
    #  If the current version ever brakes, consider switching to the built-in
    #  Link below, scroll down slightly from there.
    #   https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets
    
    if st.button('Build Confidence-curve CSV for download'):
        tmp_download_link = download_link(prob_df, 'cum_conf_curve.csv', 'CSV built! Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

    if st.button('Build parameter CSV for download'):
        tmp_download_link_params = download_link(param_df, 'parameter_values.csv', 'CSV built! Click here to download your data!')
        st.markdown(tmp_download_link_params, unsafe_allow_html=True)

    st.markdown("___")

# ----------
# App footer
# ----------

st.markdown("___")

st.write("") 

st.write("Made with ❤️ at the [SWUNG 2021 geothermal hack-a-thon](https://softwareunderground.org/events/2021/5/13/geothermal-hackathon)")
st.write("See the [github repo](https://github.com/Geothermal-Resource-Capacity/Power-Density) for project information and contributors")
