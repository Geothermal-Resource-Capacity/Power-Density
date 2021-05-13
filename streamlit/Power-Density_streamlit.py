# -*- coding: utf-8 -*-
"""
Created on Thu May 13 09:31:30 2021

"""
import streamlit as st
import plotly.express as px
import pandas as pd

st.title('Power Density')
st.write('**1: Exploration, is it there?**') #Streamlit uses markdown for formatting


# USER INPUT REQUIRED
Ptemp = st.slider('PTemperature', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Ptemp')
Pperm = st.slider('PPermeability', value=65, min_value=1, max_value=100,step=1, format='%i%%', key='Pperm')
Pchem = st.slider('Pchemistry', value=95, min_value=1, max_value=100,step=1, format='%i%%', key='Pchem')
Ptemp /= 100 #Keep things in decimal percent, but display in percent.
Pperm /= 100
Pchem /= 100

POSexpl = Ptemp * Pperm * Pchem
print("Probability of exploration success = {:.0f}%".format(POSexpl*100))
# Could potentially code in user option to adjust number of decimal places for POS

st.write(f'{Ptemp} \* {Pperm} * {Pchem} = Probability of exploration success {POSexpl*100}%')

#Plotly test
expl_dict = {'Prob':['Ptemp','Pperm','Pchem'], 'Values':[Ptemp, Pperm, Pchem]}
exploration_df = pd.DataFrame(data=expl_dict)

fig = px.bar(data_frame = exploration_df, y='Prob', x='Values', orientation='h', range_x=[0,1])
st.plotly_chart(fig)