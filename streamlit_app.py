import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
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

# import requests


# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # output it in the screen as a table
    return  fruityvice_normalized

# New Section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    # Course  Lesson 9: Streamlit - Using APIs & Variables  🥋 Variables in Streamlit  ▪️
    # 🥋 Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
        
except URLError as e:
    streamlit.error()
    
# streamlit.write('The user entered ', fruit_choice)

# Course  Lesson 12: Streamlit, but with Snowflake Added  🥋 Import Snowflake Package into Your App  ▪️
# 🥋 Check to Confirm the Snowflake Connector Package Will Add Successfully
# Now, switch back to your streamlit_app.py file and add this line. The requirements.txt file you just added to your project tells Streamlit what libraries you plan to use in your project so it can add them in advance.
# The line shown below will tell your py file to use the library you added to the project. 

# 🥋 Add a STOP Command to Focus Our Attention
# don't run anything past here while we troubleshoot
streamlit.stop()

# Course  Lesson 12: Streamlit, but with Snowflake Added  🥋 Connect to Snowflake from Streamlit  ▪️
# 🥋 Let's Query Our Trial Account Metadata 

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
# streamlit.text("Hello from Snowflake:")
# streamlit.text(my_data_row)

# Course  Lesson 12: Streamlit, but with Snowflake Added  🥋 Query a Snowflake Table from Streamlit  ▪️
# 🥋 Let's Query Some Data, Instead

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall() # fetches only one row instead of all rows: my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)
    
    
# Course  Lesson 12: Streamlit, but with Snowflake Added  🎯 Streamlit Challenge Lab!  ▪️
# 🎯 Can You Add A Second Text Entry Box? 
# Allow the end user to add a fruit to the list
add_my_fruit = streamlit.text_input('What would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')");
