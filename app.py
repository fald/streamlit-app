# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import numpy as np

#########
# CONFIG
#########
DATA_URL = "./Motor_Vehicle_Collisions_-_Crashes.csv"
NROWS = 150


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
    injured_people = st.slider("Number of people injured in vehicle collisions", 0, 19)
    st.map(data.query('number_of_persons_injured >= @injured_people'))
    #st.write(data.columns.values)
    
    
    
    
    
    
    
    
    
    
    
    
    
    