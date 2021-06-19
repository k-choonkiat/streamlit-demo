import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
import json

#importing the data for weather 
weather_data = requests.get("https://api.data.gov.sg/v1/environment/pm25").json()
weather_data = pd.DataFrame.from_dict(weather_data)

st.title('Weather and environment application')

st.write(weather_data)

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


left_column, right_column = st.beta_columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.beta_expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)