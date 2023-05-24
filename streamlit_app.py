import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# 🥋 Choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# 🥋 Choose a Few Fruits to Set a Good Example
# We want to filter the table data based on the fruits a customer will choose, so we'll pre-populate the list to set an example for the customer. 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# 🥋 Filter the Table Data
# We'll ask our app to put the list of selected fruits into a variable called fruits_selected. Then, we'll ask our app to use the fruits in our fruits_selected list to pull rows from the full data set (and assign that data to a variable called fruits_to_show). Finally, we'll ask the app to use the data in fruits_to_show in the dataframe it displays on the page. 

fruits_to_show = my_fruit_list.loc[fruits_selected]
# If you want to know more about pandas.dataframe.loc[ ], you find more information here: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html 
    
# Display the table on the page.
# original logic: streamlit.dataframe(my_fruit_list) but changed to the one below as it is dependant on the pick list.
streamlit.dataframe(fruits_to_show)


#New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
# Course  Lesson 9: Streamlit - Using APIs & Variables  🥋 Variables in Streamlit  ▪️
# 🥋 Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
# This line is deleted: streamlit.text(fruityvice_response.json()) # just writes the data to the screen


# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# output it in the screen as a table
streamlit.dataframe(fruityvice_normalized)
