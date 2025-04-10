# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#Import "col" (column function)
from snowflake.snowpark.functions import col
#Setup API Requests
import requests

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

#To connect the script from GitHub to Snowflake, from SIS no SniS
cnx = st.connection("snowflake")
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the Fruits You Want in Your Custom Smoothie!")

# create a text input for customer name
name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be: ', name_on_order)

#create a select Box for fruits
# option = st.selectbox(
#     "What is your favorite fruit",
#     ("Strawberries", "Banana", "Peaches"),
# )

# st.write("You selected:", option)

#List with different fruit imported
#session = get_active_session()
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'), col('search_on')) #only select column Fruit_name
my_dataframe = session.table("smoothies.public.fruit_options").select(col('search_on')) #only select column Fruit_name
st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#create a multiselect menu
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections = 5
)

# If Ingredients are selected, put them in a string and add them to the orders table
if ingredients_list: #if List is NULL
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    #Convert list into a string
    ingredients_string = ''
    #st.text(ingredient_string)
    
    #FOR LOOP to add each selection of fruit to the string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    # st.write(ingredients_string)
    
    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    st.write(my_insert_stmt)
    #Streamlit Stop command for testing
    #st.stop()

    #Insert a Submit Button, upon which selection is entered into Orders table
    time_to_insert = st.button('Submit Order')
    
    # Insert the Order into Snowflake
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        #Confirmation that smoothie is ordered
        st.success('Your Smoothie is ordered!', icon="✅")

#Setup API Requests
# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)




























