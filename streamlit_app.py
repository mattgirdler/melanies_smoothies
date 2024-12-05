# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customise your smoothie! 🥤")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

cnx = st.connection("snowflake") 
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
st.stop()

name_on_order = st.text_input("Name on smoothie")

ingredients_list = st.multiselect(
    "Choose up to five ingredients",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit in ingredients_list:
        try:
            search_on = session.table("smoothies.public.fruit_options").select(col("search_on").
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        st.subheader(fruit + " Nutrition Information")
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        ingredients_string += fruit + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
