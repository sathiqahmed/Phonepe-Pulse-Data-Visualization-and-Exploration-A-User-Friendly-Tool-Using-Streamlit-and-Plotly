import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
from plotly.subplots import make_subplots
import plotly.graph_objects as g
import mysql.connector
from sqlalchemy import create_engine ,text
import seaborn as sns
from PIL import Image

st.set_page_config(page_title="Phonepe_Pulse", layout="wide", initial_sidebar_state="expanded",)
                   
st.markdown(
    """
    <style>
    body {
        font-family: serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#display 
st.title(":violet[Phonepe Pulse Data Visualization]")

st.markdown("PhonePe Pulse is a comprehensive data platform that provides insights into India's consumer spending patterns across multiple categories such as groceries, fuel, dining, travel, and more. The platform aggregates data from over 500 million transactions processed on the PhonePe app, making it one of the largest sources of digital transaction data in India.")


image = Image.open(r"C:\Users\win10\Desktop\Phonepe\phone.jpg")
st.image(image)




# Connect to the MYSQL database
db = mysql.connector.connect(host="localhost",
                             user="root",
                             password="mnbvvbnmmnbv",
                             database="phonepe_pulse_data")


#Define the SQL queries for each table:
agg_trans_query = "SELECT * FROM my_aggregated_transaction"
agg_users_query = "SELECT * FROM my_aggregated_user"
map_trans_query = "SELECT * FROM my_map_transac"
map_users_query = "SELECT * FROM my_map_users"
top_trans_query = "SELECT * FROM my_top_transaction"
top_users_query = "SELECT * FROM my_top_user"


# Load the data into Pandas dataframes
agg_trans = pd.read_sql(agg_trans_query, con=db)
agg_users = pd.read_sql(agg_users_query, con=db)
map_trans = pd.read_sql(map_trans_query, con=db)
map_users = pd.read_sql(map_users_query, con=db)
top_trans = pd.read_sql(top_trans_query, con=db)
top_users = pd.read_sql(top_users_query, con=db)



#Display Page View: 
st.title(":violet[Data Analytics]")


#List the India State name
States = ['Andaman & Nicobar','Andhra Pradesh','Arunanchal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadara & Nagar Havelli',
          'Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep','Madhya Pradesh','Maharashtra','Manipur','Meghalaya',
          'Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh',
          'Uttarakhand','West Bengal']

# Define a dictionary of state name replacements
state_replacements = {
    'andaman-&-nicobar-islands': 'Andaman & Nicobar Island','andhra-pradesh': 'Andhra Pradesh', 'arunachal-pradesh': 'Arunanchal Pradesh','assam': 'Assam',
    'bihar': 'Bihar','chandigarh': 'Chandigarh','chhattisgarh': 'Chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu': 'Dadara & Nagar Havelli','delhi': 'NCT of Delhi',
    'goa': 'Goa','gujarat': 'Gujarat','haryana': 'Haryana','himachal-pradesh': 'Himachal Pradesh','jammu-&-kashmir': 'Jammu & Kashmir', 'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka','kerala': 'Kerala','ladakh': 'Ladakh','lakshadweep': 'Lakshadweep', 'madhya-pradesh': 'Madhya Pradesh', 'maharashtra': 'Maharashtra',
    'manipur': 'Manipur','meghalaya': 'Meghalaya','mizoram': 'Mizoram','nagaland': 'Nagaland','odisha': 'Odisha','puducherry': 'Puducherry','punjab': 'Punjab',
    'rajasthan': 'Rajasthan','sikkim': 'Sikkim','tamil-nadu': 'Tamil Nadu','telangana': 'Telangana','tripura': 'Tripura','uttar-pradesh': 'Uttar Pradesh','uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal',
}

# Replace state names in each dataframe
for tables in ['agg_trans', 'agg_users', 'map_trans', 'map_users', 'top_trans', 'top_users']:
    df = globals()[tables]  # Get the dataframe by name
    df['state'] = df['state'].replace(state_replacements)

#FUNCTION BLOCKS
def indiamap():
    c= map_trans.groupby(["state","year"]).sum()
    c.reset_index(inplace = True)
    return c 

def transName():
    p= map_trans.groupby(["state","year","transaction_count","total_amount"]).sum()
    p.reset_index(inplace = True)
    return p

def trantype():
    t= agg_trans.groupby(["state","year","transaction_type","transaction_count","total_amount"]).sum()
    t.reset_index(inplace= True)
    return t

def mapUser():
    u= map_users.groupby(["state","year"]).sum()
    u.reset_index(inplace = True)
    return u

def aggTrans(option1,option2,option3):
    a= agg_trans[(agg_trans.state == option1) & (agg_trans.year == option2) & (agg_trans.quarter == option3)]
    a.reset_index(inplace = True)
    return a

def mapTrans(option1,option2,option3):
    mt= map_trans[(map_trans.state == option1) & (map_trans.year == option2) & (map_trans.quarter == option3)]
    mt.reset_index(inplace = True)
    return mt

def mapUserState(option1,option2,option3):
    au= map_users[(map_users.state == option1) & (map_users.year == option2) & (map_users.quarter == option3)]
    au.reset_index(inplace = True)
    return au


#ADD OPTION MENU

with st.sidebar:
  selected = option_menu(menu_title=None, options=["India Wise","State Wise","Top 10 Wise"], orientation="vertical")         

# Code or map page
  if selected=="India Wise":
    radio_button = ["Transactions","Users"]
    option = st.radio("Which type of visualisation you need ", radio_button, index=1)

    
    if option == "Transactions":
        
     option8 = st.selectbox(
      'Select the Drop',("transaction_count","total_amount"))
    
    if option == "Users":
      option8 = st.selectbox(
      'Select the drop',("registered_users","apps_opened"))

  
# Code for statewise page
  if selected=="State Wise":
    radio_button = ["Transactions","Users"]
    option = st.radio("Which visualisation you Need", radio_button, index=1)

    if option == "Transactions":
     option1 = st.selectbox(
     'Select the State Name',States)

     option2 = st.selectbox(
     'Select the Year',(2018, 2019, 2020, 2021, 2022))

     option3 = st.selectbox(
     'Select the Quarter ',("Q1", "Q2", "Q3", "Q4"))

     option4 = st.selectbox(
     'Select the Drop',("transaction_count","total_amount"))
    
    if option == "Users":
      option1 = st.selectbox(
      'Select the State Name',States)

      option2 = st.selectbox(
      'Select the Year',(2018, 2019, 2020, 2021, 2022))

      option3 = st.selectbox(
      'Select the Quarter',("Q1", "Q2", "Q3", "Q4"))

      option4 = st.selectbox(
      'Select the Drop',("registered_users","apps_opened"))

  


#Button for Indian Map
if selected=="India Wise":
  if option == "Transactions":
   if st.button("Show"):
    c = indiamap()
    p = transName()  
    t= trantype()
 

    fig=px.choropleth(
       c,
       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
       featureidkey='properties.ST_NM',
       locations='state',
       color=option8,
       animation_frame='year',
       color_continuous_scale='twilight',
       height=500,
       width=800
      )
      
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin=dict(l=60, r=60, t=50, b=50))

    st.write("Transactions")
    st.write(fig)

    pi = px.bar(p, x="state", y=option8,animation_frame= 'year' ,title="Transaction and its Contribution with respect to State",width=900,height=700)
    st.write(pi)
  
    tt = px.bar(t, x="state", y=option8, color= "transaction_type", animation_frame= 'year' ,title="Transaction Types and its Contribution with respect to State",width=900,height=700)
    st.write(tt)
   

  if option == "Users":
   if st.button("Show"):
    u = mapUser()
  
  
      #india
    fig=px.choropleth(
       u,
       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
       featureidkey='properties.ST_NM',
       locations='state',
       color=option8,
       animation_frame='year',
       color_continuous_scale='ice',
       height=500,
       width=800
      )
      
    fig.update_geos(fitbounds="locations", visible=False)

    st.write("About User")
    st.write(fig)

#Button for statewise
if selected=="State Wise":
  if option == "Transactions":
   if st.button('Show'):
    a= aggTrans(option1,option2,option3)
    mt= mapTrans(option1,option2,option3)

   
    fig = px.choropleth(
       a,
       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
       featureidkey='properties.ST_NM',
       locations='state',
       color=option4,
       animation_frame="year",
       color_continuous_scale='aggrnyl'
      )


    fig.update_geos(fitbounds="locations", visible=False)
      
    st.write("total transaction")
    st.write(fig)

    fi = px.bar(mt, x='district_name', y=option4)

    st.write(fi)

  if option == "Users":
   if st.button('Show'):
    au= mapUserState(option1,option2,option3)

   
    fig = px.choropleth(
       au,
       geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
       featureidkey='properties.ST_NM',
       locations='state',
       color=option4,
       color_continuous_scale='ice'
      )


    fig.update_geos(fitbounds="locations", visible=False)
      
    st.write("total transaction")
    st.write(fig)  

    fi = px.bar(au, x='states', y=option4)

    st.write(fi)

# Define the number of top items to display
top_n = 10

if selected=="Top 10 Wise":

      
      # Get top 10 states and districts based on transaction count
      st.header("State Based Data")
      
      top_states = top_trans.groupby("state").sum().sort_values(by=["transaction_count"], ascending=False).head(top_n) 

      # Create animated pie chart using Plotly Express
      fig = px.pie(
      top_states.reset_index(),
      names="state",
      values="transaction_count",
      
      title="Top 10 States based on transaction_count",
      height=500,
      )

     # Show the chart in the Streamlit app
      st.plotly_chart(fig)

      top_states_users = top_users.groupby("state").sum().sort_values(by="registered_users", ascending=False).head(top_n)
      
      # Convert "state" column to string data type
      top_states_users["state"] = top_states_users.index.astype(str)

    # Create bar chart using Plotly Express
      fig = px.bar(
       top_states_users,
       x="state",
       y="registered_users",
       
       title="Top 10 States based on Registered_users ",
       height=500,
       )
 
     # Show the chart in the Streamlit app
      st.plotly_chart(fig)
      
     
     #District Based
      st.header("District Based Data")
      top_districts_user = top_users.groupby("districts").sum().sort_values(by="registered_users", ascending=False).head(top_n)

      
      # Create animated pie chart using Plotly Express
      fig = px.pie(
      top_districts_user.reset_index(),
      names="districts",
      values="registered_users",
      title="Top 10 Districts based on Registered Users",
      height=500,
      )

     # Show the chart in the Streamlit app
      st.plotly_chart(fig)
    
      top_districts= top_trans.groupby("districts").sum().sort_values(by="transaction_count", ascending=False).head(top_n) 

      # Convert "districts" column to string data type
      top_districts["districts"] = top_districts.index.astype(str)

    # Create bar chart using Plotly Express
      fig = px.bar(
       top_districts,
       x="districts",
       y="transaction_count",
       
       title="Top 10 Districts based on Transaction Count",
       height=500,
       )
 
     # Show the chart in the Streamlit app
      st.plotly_chart(fig)










      








      
      
           
   
