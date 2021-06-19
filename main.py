import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
import json

#importing the data for weather 
pm_data = requests.get("https://api.data.gov.sg/v1/environment/pm25").json()
region_info = pd.DataFrame.from_dict(pm_data["region_metadata"])
region_info = pd.concat([region_info.drop(['label_location'],axis=1),region_info['label_location'].apply(pd.Series)],axis=1)
pm_info = pd.DataFrame.from_dict(pm_data['items'][0])
pm_info = pd.concat([pm_info.drop(['readings'],axis=1),pm_info['readings'].apply(pd.Series)],axis=1)
#pre-processing of data


st.title('Weather and environment application')

st.map(region_info)

st.header("The raw data as tables")
st.subheader("Region data")
st.write(region_info)
st.subheader("PM data")
st.write(pm_info)


expander = st.beta_expander("What is this")
expander.write("A test project I wanted to create to test out Streamlit :)")
expander = st.beta_expander("What is my end goal?")
expander.write("A simple app that will dislpay PSI and also weather data and maybe even with alert systems")
expander = st.beta_expander("To do:")
expander.write("add weather data, add UV data")