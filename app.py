import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium

@st.cache_data
def load_data():
    data = pd.read_csv("data/data.csv")
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

price=st.slider('Property Price', min_value=1990000, max_value=2155000, value=2040000)
area=st.slider('Area', min_value=7150, max_value=20000, value=13000)

potential=0.0
water_proximity=0.0
road_proximity=0.0
airport_proximity=0.0
earthquake=0.0
flood=0.0
port_proximity=0.0
hospital_proximity=0.0



#section that only opens if you click button to reveal the advanced options and reteract if you click again
if st.radio("Would you like to see advanced options?", ('No', 'Yes')) == 'Yes':
    potential=st.sidebar.slider('Potential for Expansion', min_value=0.0, max_value=1.0, value=0.5)
    water_proximity=st.sidebar.slider('Proximity to Major Water Bodies', min_value=1.0, max_value=10.0, value=5.5)
    road_proximity=st.sidebar.slider('Proximity to Roadways', min_value=1.0, max_value=10.0, value=4.5)
    airport_proximity=st.sidebar.slider('Proximity to Airports', min_value=1.0, max_value=10.0, value=5.5)
    earthquake=st.sidebar.slider('Earthquake Likelihood', min_value=0.0, max_value=1.0, value=0.5)
    flood=st.sidebar.slider('Flood Likelihood', min_value=0.0, max_value=1.0, value=0.5)
    port_proximity=st.sidebar.slider('Proximity to Ports', min_value=1.0, max_value=10.0, value=5.5)
    hospital_proximity=st.sidebar.slider('Proximity to Hospitals', min_value=1.0, max_value=10.0, value=4.5)
else:
    potential=0.0
    water_proximity=0.0
    road_proximity=0.0
    airport_proximity=0.0
    earthquake=0.0
    flood=0.0
    port_proximity=0.0
    hospital_proximity=0.0
    

#filtering the data based on the user input to be around the selected factors

df=df[(df['Price']<=price)]
df=df[(df['Area']<=area)]
df=df[(df['Potential_for_Expansion']>=potential)]
df=df[(df['Proximity_to_Major_Water_Body']>=water_proximity)]
df=df[(df['Proximity_to_Roadways']>=road_proximity)]
df=df[(df['Proximity_to_Airports']>=airport_proximity)]
df=df[(df['Earthquake_Likelihood']>=earthquake)]
df=df[(df['Flood_Likelihood']>=flood)]
df=df[(df['Proximity_to_Ports']>=port_proximity)]
df=df[(df['Proximity_to_Hospitals']>=hospital_proximity)]
df=df.sort_values(by=['Price'], ascending=False)


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