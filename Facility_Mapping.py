import folium
from geopy.distance import geodesic
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import math


APP_TITLE = "Kenya health Facilities Mapping"
APP_SUBTITLE = "The map shows all of Kenya's health facilities with their  corresponding Levels and highlights Level 4"

def load_data(string:str):
    """
    Load the data from the csv file
    """
    hospitals = pd.read_csv(string)  

    
    hospitals_gvt = hospitals[hospitals.latitude.isnull()!=True]

    return hospitals_gvt


def display_map():
    
    attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, <a href="http://viewfinderpanoramas.org">SRTM</a>'
    )
    tiles = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
    center = [-0.023559, 37.9061928]
    map_kenya = folium.Map(location=center,tiles=tiles,attr=attr, zoom_start=6 )

    return map_kenya

mapper = display_map()

def plot_points(point):
    folium.Circle(location=[point.latitude, point.longitude],
                        radius=5).add_to(mapper)
    
def all_points(hospy,km_chooser):
    
    
    for index, hospy in hospy.iterrows():
        location = [hospy['latitude'], hospy['longitude']]
        icon=folium.Icon(color='green')
        folium.Marker(location, 
                      icon = icon,
                      popup = f"Name: {hospy.facility} Keph Level: {hospy.keph_level}").add_to(mapper)
        
        folium.Circle(location,
                    radius=km_chooser*1000,
                    color = "green",
                    popup = f"{km_chooser}Radius, Name: {hospy.facility}, Keph Level: {hospy.keph_level}").add_to(mapper)
    
 



def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.subheader(APP_SUBTITLE)

    # LOAD DATA
    hospitals_gvt = load_data("hospital geo_codes_cleanest.csv")

    # st.selectbox("Select the Level interested in seeing", hospitals_gvt['keph_level'].unique())

    kms = [10,15,20]
    facility_level = 'Level 4'

    kms_chooser = st.sidebar.selectbox('Select the number of Kilometres for the radius', kms)

    select_all = st.sidebar.checkbox('Select All Counties')
    if select_all:
        county = hospitals_gvt['county'].unique()
        hospy = hospitals_gvt[(hospitals_gvt['keph_level']==facility_level)& (hospitals_gvt['county'].isin(county))]
    else:
        county = st.sidebar.selectbox('Choose a County', hospitals_gvt['county'].unique())
        hospy = hospitals_gvt[(hospitals_gvt['keph_level']==facility_level)& (hospitals_gvt['county']==county)]
    # county = st.sidebar.selectbox('Choose a County', hospitals_gvt['county'].unique())
    # subcounty = st.sidebar.multiselect('Choose a Sub County', hospitals_gvt['sub_county'].unique())
    
    # county = 'Narok'                                                  to be added if need be
    metric_title = f"{facility_level} Facilities:"
    metric_title2 = f"Total Number of Health Facilities in {county} is:"

    if kms_chooser == 10:
        dd = hospitals_gvt['10km_to_level4'].sum()
        d1 = hospy['10km_to_level4'].sum()
        hh = hospitals_gvt[hospitals_gvt['10km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)

    elif kms_chooser == 15:
        dd = hospitals_gvt['15km_to_level4'].sum()
        d1 = hospy['15km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['15km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)
    elif kms_chooser == 20:
        dd = hospitals_gvt['20km_to_level4'].sum()
        d1 = hospy['20km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['20km_to_level4'] != 0]['facility'].reset_index()
        hh.index = range(1, hh.shape[0]+1)


    metric_title3= f"""Total Number of Level 4 far from level 2 and 3 at {kms_chooser} radius are:"""
    
    st.subheader(f"The Level 4 Health Facilities that do not have a level 2 or 3 health facility within the {kms_chooser}kms : are")
    st.write(hh)
    
    
    st.subheader(f"Nation Wide Facts")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(metric_title2, "{:,}".format(hospitals_gvt.shape[0]))
    with col2:
        st.metric(metric_title, "{:,}".format(hospitals_gvt[hospitals_gvt['keph_level']=='Level 4'].shape[0]))
    
    st.subheader(f"Distance Metrics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(metric_title3, dd)
    with col2:
        st.metric(f"Total Number of Level 4  far from level 2 and 3 in {county} is:", d1)

    
    


    # DISPLAY FILTERS AND MAP
    
    st.subheader(f"Map of {facility_level} Health Facilities")
    hospitals_gvt.apply(plot_points, axis =1)
    all_points(hospy,kms_chooser)
    st_folium(mapper)
    



    
    #

if __name__ == "__main__":
    main()