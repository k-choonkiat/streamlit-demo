import streamlit as st
import numpy as np
import pandas as pd
import requests
from PIL import Image
import pydeck as pdk

#importing the data for weather 
pm_data = requests.get("https://api.data.gov.sg/v1/environment/pm25").json()
region_info = pd.DataFrame.from_dict(pm_data["region_metadata"])
region_info = pd.concat([region_info.drop(['label_location'],axis=1),region_info['label_location'].apply(pd.Series)],axis=1)
pm_info = pd.DataFrame.from_dict(pm_data['items'][0])
pm_info = pd.concat([pm_info.drop(['readings'],axis=1),pm_info['readings'].apply(pd.Series)],axis=1)
uv_data = requests.get("https://api.data.gov.sg/v1/environment/uv-index").json()

# pre-processing of data
# pm processing
midpoint = (np.average(region_info['latitude']), np.average(region_info['longitude']))
pm = pm_info[['west','east','central','south','north']].T.reset_index()
pm = pm.rename(columns={"index":"region"})
df = region_info.merge(pm,left_on="name",right_on="region")
df = df.drop(['region'],axis=1)
# uv processing
uv_info = pd.DataFrame.from_dict(uv_data['items'][0])
uv_info = uv_info['index'].apply(pd.Series)
uv_curr= uv_info.iloc[1].value

st.title('Weather and environment application')

st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=midpoint[0],
         longitude=midpoint[1],
         zoom=11,
         pitch=50,
     ),
     layers=[

        pdk.Layer(
             'ScatterplotLayer',
             data=df,
             get_position='[longitude, latitude]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
         pdk.Layer(
            "ColumnLayer",
            data=df,
            get_position='[longitude, latitude]',
            get_elevation='[pm25_one_hourly]',
            elevation_scale=100,
            radius=200,
            get_fill_color='[100,30,100,255]',
            pickable=True,
            auto_highlight=True,
)
     ],
 ))

area= st.text_input(label="Enter an area",value='north')
st.write("The pm for the ", area, " is ", df[df['name']==area]['pm25_one_hourly'])
st.subheader("The current UV value is ")
st.write(uv_curr)

st.subheader("PM info chart")
image = Image.open('images/pm.jpg')
st.image(image,caption='Guidance for PM levels')
image_uv = Image.open('images/uv.png')
st.image(image_uv,caption='Guidance for UV levels')

st.header("The raw data as tables")
st.subheader("Combined table")
st.write(df)
st.subheader("Region data")
st.write(region_info)
st.subheader("PM data")
st.write(pm_info)
st.subheader("The raw data for UV levels")
st.write(uv_info)

expander = st.beta_expander("What is this")
expander.write("A test project I wanted to create to test out Streamlit :)")
expander = st.beta_expander("What is my end goal?")
expander.write("A simple app that will dislpay PSI and also weather data and maybe even with alert systems")
expander = st.beta_expander("To do:")
expander.write("add weather data, add UV data, build data engineering pipelines")