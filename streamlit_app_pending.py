# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#Import "col" (column function)
from snowflake.snowpark.functions import col, when_matched 

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write("Orders that need to be filled")

#create a select Box for completed
# option = st.radio(
#     "Is Order filled?",
#     ["true", "false"],
# )

# st.write("You selected:", option)


#List with different fruit imported
#session = get_active_session()
#For connection of github script to streamlit
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect() #Only collect orders that are not filled (false)



if my_dataframe:
    #Create a dataframe that is editable (Tickbox in Table)
    editable_df = st.data_editor(my_dataframe)
    #Submit Button
    submitted = st.button('Submit')
    if submitted:
        
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)

        try:
            og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
            st.success("Someone clicked the button.", icon='👍')
        except:
            st.write("Something went wrong.")
else:
    st.success('There are no pending orders right now', icon='👍' )


#New Section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = request.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
























