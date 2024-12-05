# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("🥤 Customise your smoothie! 🥤")
st.write(
    """Choose the fruits you want in your custom smoothie!"""
)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

name_on_order = st.text_input("Name on smoothie")

ingredients_list = st.multiselect(
    "Choose up to five ingredients",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")