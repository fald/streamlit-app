# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import numpy as np
import pydeck as pdk

#########
# CONFIG
#########
DATA_URL = "./Motor_Vehicle_Collisions_-_Crashes.csv"
NROWS = 1000


def display_intro():
    title = "Motor Vehicle Collisions (NYC)"
    subtitle = "This application is a Streamlit dashboard that can be used to analyze motor vehicle collisions in NYC"
    credit = "This is a follow-along of a guided project provided by Coursera titled: 'Build a Data Science Web App with Streamlit and Python', run by Snehan Kekre"
    
    st.title(title)
    st.markdown("## " + subtitle)
    st.markdown("#### " + credit + "\n#")


@st.cache(persist=True)
def load_data(nrows):
    # Can't be loading in a 500MB file into ram or nothin'
    data = pd.read_csv(
            DATA_URL, nrows=nrows, 
            parse_dates={'date/time': ['CRASH DATE', 'CRASH TIME']})
    # Will need Lat/Lon to not break the map
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)

    cols = data.columns
    cols = cols.map(lambda x: x.replace(' ', '_'))
    data.columns = cols
    
    return data
    

if __name__ == "__main__":
    display_intro()
    data = load_data(NROWS)
    
    if st.checkbox("Show raw data"):
        st.subheader("Raw Data")
        st.write(data)
        
    st.header("Where are the most people injured in NYC?")
    injured_people = st.slider("Number of people injured in an instance of vehicle collision", 0, 19)
    # Strictly speaking, it doesn't seem like isolating the lat/lon is necessary for st.map
    result_where = data.query('number_of_persons_injured >= @injured_people')[['latitude', 'longitude']] 
    st.write("Number of cases: " + str(len(result_where.index)))
    st.map(result_where)
    #st.write(data.columns.values)
    
    st.header("What time of day do most collisions occur?")
    hour = st.slider("Hour", 0, 23)
    result_when = data[data['date/time'].dt.hour == hour]
    st.markdown("Collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    num_results = len(result_when.index)
    st.write("\tNumber of cases: " + str(num_results))
    mid_point = (np.average(result_when['latitude']), np.average(result_when['longitude'])) if num_results > 0 else (0, 0)
    
    st.write(result_when)    
    
    st.write(pdk.Deck(
        #map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": mid_point[0],
            "longitude": mid_point[1],
            "zoom": 11,
            "pitch": 50
        },
        layers = [
            pdk.Layer(
                "HexagonLayer",
                data=result_when[['date/time', 'latitude', 'longitude']],
                get_position=['longitude', 'latitude'],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=40,
                elevation_range=[100, 200],
            ),
        ],
    ))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    