import folium
from geopy.distance import geodesic
import pandas as pd
import streamlit as st
import geopandas as gpd
from streamlit_folium import st_folium
from branca.element import Template, MacroElement
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

@st.cache_data
def loading_shp(string:str):
    """
    Load the data from the csv file
    """
    shp = gpd.read_file(string)  

    return shp


def color_for_keph_level(keph_level):
    if keph_level == 'Level 4':
        return 'blue'
    elif keph_level == 'Level 5':
        return 'red'
    elif keph_level =='Level 2':
        return 'blue'  
    elif keph_level =='Level 3':
        return 'cyan'


def display_map():
    center = [-0.023559, 37.9061928]
    map_kenya = folium.Map(location=center, zoom_start=6 )

    return map_kenya

mapper = display_map()

def plot_points(hospitals_gvt:pd.DataFrame):
    colors = {
        'Level 2':'blue',
        'Level 3':'cyan',
        'Level 4': 'blue',  # Example: KEPH Level 4 is blue
        'Level 5': 'orange', # Example: KEPH Level 5 is green
        'Level 6': 'red'    # Example: KEPH Level 6 is red
    }

    # Adding markers to the map
    for idx, row in hospitals_gvt.iterrows():
        keph_level = row['keph_level']
        color = colors.get(keph_level, 'gray')  # Default to gray if no matching level
        
        folium.Circle(
            location=[row['latitude'], row['longitude']],
            popup=f"Facility: {hospitals_gvt['facility']},Hospital Level: {keph_level}",
            color=color
        ).add_to(mapper)

    
def all_points(hospy,km_chooser):
    
    
    for index, hospy in hospy.iterrows():
        location = [hospy['latitude'], hospy['longitude']]
        folium.Marker(location, 
                      icon=folium.Icon(color=color_for_keph_level(hospy['keph_level'])),
                      popup = f"Name: {hospy.facility} Keph Level: {hospy.keph_level}").add_to(mapper)
        
        folium.Circle(location,
                    radius=km_chooser*1000,
                    color = color_for_keph_level(hospy['keph_level']),
                    popup = f"{km_chooser}Radius, Name: {hospy.facility}, Keph Level: {hospy.keph_level}").add_to(mapper)
    
 



def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.subheader(APP_SUBTITLE)

    # LOAD DATA
    hospitals_gvt = load_data("hospital geo_codes_cleanest1.csv")

    # st.selectbox("Select the Level interested in seeing", hospitals_gvt['keph_level'].unique())

    kms = [5,7.5,10,12.5,15,17.5,20]
    facility_level = 'Level 4'

    kms_chooser = st.sidebar.selectbox('Select the number of Kilometres for the radius', kms)

    hospitals_ownership = st.sidebar.selectbox('Choose Ownership', hospitals_gvt['Ownership'].unique())

    Hospital_level = st.sidebar.selectbox('Choose Health Facility Level', hospitals_gvt['keph_level'].unique())

    select_all = st.sidebar.checkbox('Select All Counties')
    if select_all:
        county = hospitals_gvt['county'].unique()
        hospy = hospitals_gvt[(hospitals_gvt['keph_level']==facility_level)& (hospitals_gvt['county'].isin(county))]
    else:
        county = st.sidebar.selectbox('Choose a County', hospitals_gvt['county'].unique())
        hospy = hospitals_gvt[(hospitals_gvt['keph_level']==facility_level)& (hospitals_gvt['county']==county)&(hospitals_gvt['Ownership']==hospitals_ownership)]
    # county = st.sidebar.selectbox('Choose a County', hospitals_gvt['county'].unique())
    # subcounty = st.sidebar.multiselect('Choose a Sub County', hospitals_gvt['sub_county'].unique())
    
    # county = 'Narok'                                                  to be added if need be
    metric_title = f"{facility_level} Facilities:"
    metric_title2 = f"Total Number of Health Facilities in {county} is:"

    if kms_chooser == 5:
        dd = hospitals_gvt['5km_to_level4'].sum()
        d1 = hospy['5km_to_level4'].sum()
        hh = hospitals_gvt[hospitals_gvt['5km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)

    elif kms_chooser == 7.5:
        dd = hospitals_gvt['7_5km_to_level4'].sum()
        d1 = hospy['7_5km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['7_5km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)

    elif kms_chooser == 10:
        dd = hospitals_gvt['10km_to_level4'].sum()
        d1 = hospy['10km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['10km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)

    elif kms_chooser == 12.5:
        dd = hospitals_gvt['12_5km_to_level4'].sum()
        d1 = hospy['12_5km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['12_5km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)

    elif kms_chooser == 15:
        dd = hospitals_gvt['15km_to_level4'].sum()
        d1 = hospy['15km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['15km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)
    
    elif kms_chooser == 17.5:
        dd = hospitals_gvt['17_5km_to_level4'].sum()
        d1 = hospy['17_5km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['17_5km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)
    
    elif kms_chooser == 20:
        dd = hospitals_gvt['20km_to_level4'].sum()
        d1 = hospy['20km_to_level4'].sum()

        hh = hospitals_gvt[hospitals_gvt['20km_to_level4'] != 0]['facility']
        hh.index = range(1, hh.shape[0]+1)


    metric_title3= f"""Total Number of Level 4 isolated at {kms_chooser} radius are:"""
    
    st.subheader(f"The Level 4 isolated Health Facilities in a {kms_chooser}km radius : are")
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
        st.metric(f"Isolated Level 4 in  {county} are:", d1)

    
    # DISPLAY FILTERS AND MAP
    
    st.subheader(f"Map of {Hospital_level} Health Facilities")
    plot_points(hospitals_gvt[(hospitals_gvt['keph_level']==Hospital_level)&(hospitals_gvt['Ownership']==hospitals_ownership)])
    all_points(hospy,kms_chooser)
    st_folium(mapper)
    
if __name__ == "__main__":
    main()