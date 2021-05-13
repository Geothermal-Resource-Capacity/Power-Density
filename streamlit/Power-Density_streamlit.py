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


# Exploration portion of inputs ######################
col1, col2, col3 = st.beta_columns(3) # Show sliders in 3 columns

st.write("## Exploration Parameters")
Ptemp = col1.slider('PTemperature', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Ptemp')
Pperm = col2.slider('PPermeability', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Pperm')
Pchem = col3.slider('Pchemistry', value=95, min_value=1, max_value=100,step=1, format='%i%%', key='Pchem')
Ptemp /= 100 #Keep things in decimal percent, but display in percent. st isn't good about formating yet
Pperm /= 100 #  These don't need to be in the sidebar, but I want them close to the input
Pchem /= 100 #  I think it makes things clearer.

#Show input results ###################################
POSexpl = Ptemp * Pperm * Pchem
print("Probability of exploration success = {:.0f}%".format(POSexpl*100))
# Could potentially code in user option to adjust number of decimal places for POS

st.write(f'{Ptemp} \* {Pperm} * {Pchem} = Probability of exploration success {POSexpl*100}%')

#Plotly test
expl_dict = {'Prob':['Ptemp','Pperm','Pchem'], 'Values':[Ptemp, Pperm, Pchem]}
exploration_df = pd.DataFrame(data=expl_dict)

fig = px.bar(data_frame = exploration_df, y='Prob', x='Values', orientation='h', range_x=[0,1])
st.plotly_chart(fig)



##Appraisal and dev inputs
st.markdown("___")
st.write("## Appraisal and Dev Parameters")

#Cumulative confidence of optimistic case
Opt_case = st.slider('Optimistic case', value=10, min_value=1, max_value=100,step=1, format='%i%%', key='opt_case')
Opt_case /= 100 #decimal percent

#probably should add a message/try catch that this must be numeric:
Tmax = int(st.text_input("Startup averages temperature for P90 reserves (degrees C)", 280))
Tmin = int(st.text_input("Minimum temperature for the P10 reservoir (degrees C)", 250))

# USER INPUT REQUIRED
# Area > 250 deg C in km2

st.write("**Area > 250 degrees C, in KM^2**")
col1.Area_P90 = int(st.text_input("Area P90:", 1))
col2.Area_P10 = int(st.text_input("Area P10:", 10))

# USER INPUT REQUIRED
st.write("**Power Density 250 to 280 deg C (MWe/km2)**")
PowerDens_P90 = int(st.text_input("Power density P90:", 10))
PowerDens_P10 = int(st.text_input("Power Density P10:", 24))


