import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

st.set_page_config(page_title='SupplySync', page_icon=':earth_americas:')

@st.cache_data
def load_data():
    data = pd.read_csv("Data/Final_data.csv")
    return data
df=load_data()

st.markdown("""
    <style>
    /* Hide the link button */
    .stApp a:first-child {
        display: none;
    }
    
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)

#latitude,longitude,price,area,potential_for_expansion,earthquake_likelihood,flood_likelihoodProximity to roadways, proximity to airports, proximity to ports, proximity to hospitals, major water body, cutomers

st.title('SupplySync')
st.write('SupplySync is a tool to help you find the best possible locations to set up warehouses and distribution centers.')

st.write(f'### Please enter the following information to get started:')

price=st.slider('Property Price (Rs.)', min_value=85000, max_value=130000, value=106000)
area=st.slider('Area (sq. km.)', min_value=4250, max_value=6500, value=5300)

potential=df['potential_for_expansion'].max()
water_proximity=df['proximity_to_major_water_body'].max()
road_proximity=df['proximity_to_roadways'].max()
airport_proximity=df['proximity_to_airports'].max()
earthquake=df['earthquake_likelihood'].max()
flood=df['flood_likelihood'].max()
port_proximity=df['proximity_to_ports'].max()
hospital_proximity=df['proximity_to_hospitals'].max()
city_proximity=df['proximity_to_cities'].max()

warehouse_type=st.selectbox('Select the type of warehouse you are looking for:', ('All','Industrial', 'Commercial', 'Logistics', 'Retail'))

if warehouse_type=='All':
    df=df
elif warehouse_type=='Industrial':
    df=df[df['warehouse_type']=='Industrial']
elif warehouse_type=='Commercial':
    df=df[df['warehouse_type']=='Commercial']
elif warehouse_type=='Logistics':
    df=df[df['warehouse_type']=='Logistics']
elif warehouse_type=='Retail':
    df=df[df['warehouse_type']=='Retail']

#section that only opens if you click button to reveal the advanced options and reteract if you click again
if st.radio("Would you like to see advanced options?", ('No', 'Yes')) == 'Yes':
    potential=st.sidebar.slider('Potential for Expansion (Future returns in 2 years)', min_value=float(df['potential_for_expansion'].min()), max_value=float(df['potential_for_expansion'].max()), value=df['potential_for_expansion'].median())
    water_proximity=st.sidebar.slider('Proximity to Major Water Bodies (km)', min_value=float(df['proximity_to_major_water_body'].min()), max_value=float(df['proximity_to_major_water_body'].max()), value=df['proximity_to_major_water_body'].median())
    road_proximity=st.sidebar.slider('Proximity to Roadways (km)', min_value=float(df['proximity_to_roadways'].min()), max_value=float(df['proximity_to_roadways'].max()), value=df['proximity_to_roadways'].median())
    airport_proximity=st.sidebar.slider('Proximity to Airports (km)', min_value=float(df['proximity_to_airports'].min()), max_value=float(df['proximity_to_airports'].max()), value=df['proximity_to_airports'].median())
    earthquake=st.sidebar.slider('Earthquake Likelihood \n (Probability of 6+ Richter scale Earthquake)', min_value=float(df['earthquake_likelihood'].min()), max_value=float(df['earthquake_likelihood'].max()), value=df['earthquake_likelihood'].median())
    flood=st.sidebar.slider('Flood Likelihood (Probability of major water body flooding)', min_value=float(df['flood_likelihood'].min()), max_value=float(df['flood_likelihood'].max()), value=df['flood_likelihood'].median())
    port_proximity=st.sidebar.slider('Proximity to Ports (km)', min_value=float(df['proximity_to_ports'].min()), max_value=float(df['proximity_to_ports'].max()), value=df['proximity_to_ports'].median())
    hospital_proximity=st.sidebar.slider('Proximity to Hospitals (km)', min_value=float(df['proximity_to_hospitals'].min()), max_value=float(df['proximity_to_hospitals'].max()), value=df['proximity_to_hospitals'].median())
    city_proximity=st.sidebar.slider('Proximity to Major Cities (km)', min_value=float(df['proximity_to_cities'].min()), max_value=float(df['proximity_to_cities'].max()), value=df['proximity_to_cities'].median())
else:
    potential=df['potential_for_expansion'].max()
    water_proximity=df['proximity_to_major_water_body'].max()
    road_proximity=df['proximity_to_roadways'].max()
    airport_proximity=df['proximity_to_airports'].max()
    earthquake=df['earthquake_likelihood'].max()
    flood=df['flood_likelihood'].max()
    port_proximity=df['proximity_to_ports'].max()
    hospital_proximity=df['proximity_to_hospitals'].max()
    city_proximity=df['proximity_to_cities'].max()
    

#filtering the data based on the user input to be around the selected factors

df=df[(df['price']<=price)]
df=df[(df['area']<=area)]
df=df[(df['potential_for_expansion']<=potential)]
df=df[(df['proximity_to_major_water_body']<=water_proximity)]
df=df[(df['proximity_to_roadways']<=road_proximity)]
df=df[(df['proximity_to_airports']<=airport_proximity)]
df=df[(df['earthquake_likelihood']<=earthquake)]
df=df[(df['flood_likelihood']<=flood)]
df=df[(df['proximity_to_ports']<=port_proximity)]
df=df[(df['proximity_to_hospitals']<=hospital_proximity)]
df=df.sort_values(by=['price'], ascending=False)


#displaying the data
st.write(f'### Here are the top locations that match your criteria:')
df.reset_index(drop=True, inplace=True)
df.index += 1
st.dataframe(df.head(3))

st.write(f'### Here are the top locations that match your criteria on a map:')

#folium map to display the filtered data

new_df=df.head(3)
new_df=new_df[['latitude','longitude']]

if len(new_df)>0: 
    map=folium.Map(location=[df['latitude'].mean(),df['longitude'].mean()],zoom_start=10)
    for i in range(0,len(new_df)):
        folium.Marker([new_df.iloc[i]['latitude'],new_df.iloc[i]['longitude']],popup="Location "+str(i+1),icon=folium.Icon(color='red',icon='info-sign')).add_to(map)
    folium_static(map)