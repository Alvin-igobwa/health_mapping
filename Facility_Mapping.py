import folium
from geopy.distance import geodesic
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import math


APP_TITLE = "Kenya health Facilities Mapping"
APP_SUBTITLE = "The map shows all of Kenya's health facilities with their  corresponding Levels and highlights Level 4"


@st.cache_data
def load_data(string:str):
    """
    Load the data from the csv file
    """
    hospitals = pd.read_csv(string)  

    
    hospitals_gvt = hospitals[hospitals.latitude.isnull()!=True]

    return hospitals_gvt


def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two sets of (lat, lon) coordinates in kilometers.
    """
    R = 6371.0  # Earth radius in kilometers

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def hospitals_within_radius(hospital, other_hospitals, radius_km):
    """
    Find how many other hospitals are within a given radius of the hospital.
    """
    count = 0
    for other_hospital in other_hospitals:
        if haversine_distance((hospital['latitude'], hospital['longitude']), (other_hospital['latitude'], other_hospital['longitude'])) <= radius_km:
            count += 1
    return count


def display_map(hospy:pd.DataFrame, hospitals_gvt:pd.DataFrame,kms_chooser:int):
    
    attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, <a href="http://viewfinderpanoramas.org">SRTM</a>'
    )
    tiles = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
    center = [-0.023559, 37.9061928]
    map_kenya = folium.Map(location=center,tiles=tiles,attr=attr, zoom_start=6 )
    
    for index, hospitals_gvt in hospitals_gvt.iterrows():
        location = [hospitals_gvt['latitude'], hospitals_gvt['longitude']]
        folium.Circle(location, 
                            radius=5,
                            popup = f"Name: {hospitals_gvt.facility} Keph Level: {hospitals_gvt.keph_level}").add_to(map_kenya)
        
    for index, hospy in hospy.iterrows():
        location = [hospy['latitude'], hospy['longitude']]
        icon=folium.Icon(color='green')
        folium.Marker(location, 
                      icon = icon,
                      popup = f"Name: {hospy.facility} Keph Level: {hospy.keph_level}").add_to(map_kenya)
        
        folium.Circle(location,
                    radius=kms_chooser*1000,
                    color = "green",
                    popup = f"{kms_chooser} Radius, Name: {hospy.facility}, Keph Level: {hospy.keph_level}").add_to(map_kenya)
    
    st_map = st_folium(map_kenya)
    return st_map


@st.cache_data
def distances(hospitals_gvt:pd.DataFrame, facility_level, kms_chooser):
    level_4_hospitals = hospitals_gvt[hospitals_gvt['keph_level'] == facility_level]
    # Filter out Level 2 and Level 3 hospitals
    level_2_3_hospitals = hospitals_gvt[(hospitals_gvt['keph_level'] == "Level 2") | (hospitals_gvt['keph_level'] == "Level 3")]

    # Find the Level 4 hospitals that do not have any Level 2 or Level 3 hospitals within 10 km
    hospitals_no_level_2_3_nearby = []

    for _, level_4_hospital in level_4_hospitals.iterrows():
        if hospitals_within_radius(level_4_hospital, level_2_3_hospitals.to_dict('records'),kms_chooser) == 0:
            hospitals_no_level_2_3_nearby.append(level_4_hospital['facility'])

    # Print out the results
    print("Level 4 hospitals without Level 2 or Level 3 hospitals within 10 km:")
    hosis = []
    for hospital in hospitals_no_level_2_3_nearby:
        hosis.append(hospital)
    
    return hosis,hospitals_no_level_2_3_nearby
    


def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.subheader(APP_SUBTITLE)

    # LOAD DATA
    hospitals_gvt = load_data("hospital geo_codes_clean.csv")

    # st.selectbox("Select the Level interested in seeing", hospitals_gvt['keph_level'].unique())

    kms = [10,15,20]
    kms_chooser = st.selectbox('Select the number of Kilometres for the radius', kms)


    facility_level = 'Level 4'
    # county = 'Narok'                                                  to be added if need be

    

    hospy = hospitals_gvt[hospitals_gvt['keph_level']==facility_level]
    metric_title = f"Number of Health Facilities of {facility_level} is:"
    metric_title2 = f"Total Number of Health Facilities is:"
    
    st.subheader(f"Facts")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(metric_title2, "{:,}".format(hospitals_gvt.shape[0]))
    with col2:
        st.metric(metric_title, "{:,}".format(hospy.shape[0]))


    # DISPLAY FILTERS AND MAP
    
    st.subheader(f"Map of {facility_level} Health Facilities")
    display_map(hospy,hospitals_gvt, kms_chooser)

    
    # DISPLAY METRICS


    dd = distances(hospitals_gvt, facility_level, kms_chooser)
    st.write(dd[0])
    metric_title3= f"The number of Level 4 Hospitals that have no Level 2 or 3 within a {kms_chooser} radius are:"
    st.metric(metric_title3, len(dd[1]))

if __name__ == "__main__":
    main()