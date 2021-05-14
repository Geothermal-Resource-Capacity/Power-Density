# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:31:30 2021

"""
# Import libraries for viz
import streamlit as st
import plotly.express as px
import pandas as pd

#libs for computation
import numpy as np
import scipy
from scipy.stats import norm, lognorm
import matplotlib.pyplot as plt

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
print("Probability of exploration success = {:.2f}%".format(round(POSexpl*100,0)))
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

#Cumulative confidence of optimistic case
Opt_case = st.slider('Optimistic case', value=10, min_value=1, max_value=100,step=1, format='%i%%', key='opt_case')
Opt_case /= 100 #decimal percent

#probably should add a message/try catch that this must be numeric:
Tmax = int(colA.text_input("Startup averages temperature for P90 reserves (degrees C)", 280))
Tmin = int(colB.text_input("Minimum temperature for the P10 reservoir (degrees C)", 250))

# USER INPUT REQUIRED
# Area > 250 deg C in km2

st.markdown("**Area > 250 degrees C, in KM^2**")
Area_P90 = int(colA.text_input("Area P90:", 1))
Area_P10 = int(colB.text_input("Area P10:", 10))

# USER INPUT REQUIRED
st.write("**Power Density 250 to 280 deg C (MWe/km2)**")
PowerDens_P90 = int(colA.text_input("Power density P90:", 10))
PowerDens_P10 = int(colB.text_input("Power Density P10:", 24))


## CALCULATIONS ################################################


# Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)
area_nu = ((np.log(Area_P90)+np.log(Area_P10))/2)
st.write("Calculate nu and sigma for area > 250 degC (the mean and variance in log units required for specifying lognormal distributions)", area_nu)

area_sigma = (np.log(Area_P10)-np.log(Area_P90))/((norm.ppf(1-Opt_case)-(norm.ppf(Opt_case))))
st.write("Area sigma", area_sigma)

# Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)
st.write("Calculate nu and sigma for power density (the mean and variance in log units required for specifying lognormal distributions)")
powerdens_nu = ((np.log(PowerDens_P90)+np.log(PowerDens_P10))/2)
st.write("Power density nu ",powerdens_nu)

powerdens_sigma = (np.log(PowerDens_P10)-np.log(PowerDens_P90))/((norm.ppf(1-Opt_case)-(norm.ppf(Opt_case))))
st.write("Power density sigma ", powerdens_sigma)

# Calculate nu and sigma for MWe Capacity
capacity_nu = area_nu + powerdens_nu
"capacity_nu", capacity_nu

capacity_sigma = ((area_sigma**2)+(powerdens_sigma**2))**0.5
"capacity_sigma", capacity_sigma

# Calculate cumulative confidence curve for expected power capacity (epc)

prob = [0.1]
expected_power_capacity=[]
expected_development_size=[]
prob_desc = []

# Specify probability range
for i in range(1,100):
    prob.append(i)

for j in prob:
    # Calculate expected development size distribution
    eds = lognorm.ppf(j/100, capacity_sigma, loc=0, scale=np.exp(capacity_nu))
    expected_development_size.append(eds)
    # Calculate power capacity distribution
    epc = eds*POSexpl
    expected_power_capacity.append(epc)
    # Calculate 100-prob for plotting descending cumulative probability
    desc = 100-j
    prob_desc.append(desc)
    # Print results
    #print(j, epc, eds, desc)

epc = [lognorm.ppf(x/100, capacity_nu, capacity_sigma)*POSexpl for x in range(0,100)]
indx = list(np.arange(0,100))
epc_tups = list(zip(indx,epc))
prob_df = pd.DataFrame(epc_tups, columns = ['Values', 'Prob'])

fig = px.bar(data_frame = prob_df, y='Prob', x='Values', orientation='h', range_x=[0,1])
st.plotly_chart(fig)

# Line plot
fig = px.line(df2, x="Date", y="Cases")
st.plotly_chart(fig)




##### FINAL PLOTS ######################
# Plot power capacity cumulative distribution
##### better to change it to streamlit native plots I think for interactivity (hover and see value)
##### I've just ported over the notebook code for a quick placeholder
colA, colB = st.beta_columns(2) # Show sliders in 2 columns
figPowerCapacity = plt.figure()
plt.plot(expected_power_capacity, prob_desc)
plt.xlabel("Expected Power Capacity (MWe potential reserves)")
plt.ylabel("Cumulative Confidence %")
plt.title("Cumulative Confidence in Power Capacity")
colA.pyplot(fig=figPowerCapacity)


# Plot expected development size cumulative distribution
figDevSize = plt.figure()
plt.plot(expected_development_size, prob_desc)
plt.xlabel("Expected Development Size (MW)")
plt.ylabel("Cumulative Confidence %")
plt.title("Cumulative Confidence in Developed Reservoir Size")
colB.pyplot(fig=figDevSize)



