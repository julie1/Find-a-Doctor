#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests


# In[2]:


from googletrans import Translator
translator = Translator()


# In[2]:


# URL of the webpage with the HTML table
url = 'https://www.resurfacingscan.be/ortopedlistan/drutoml.htm'

# Fetch the content of the webpage
response = requests.get(url)


# In[3]:


###correct code
import pandas as pd
import requests
#from googletrans import Translator
from bs4 import BeautifulSoup

# URL of the webpage with the HTML table
url = 'https://www.resurfacingscan.be/ortopedlistan/drutoml.htm'

# Correct column names from the file
correct_column_names = [
    "orthopedic_surgeon_first_name", "orthopedic_surgeon_surname", "jpg_doctor", "born_year", "address", "street",
    "local", "city", "postal_code", "country", "phone_normal", "phone_free_of_charge", "fax", "mobile",
    "email", "homepage", "number_hr", "adjusted", "number_thr", "number_bmhr",
    "type_of_hr_prosthesis", "type_of_thr_prosthesis", "operational_technique", "anesthetic", "cement_femur_side",
    "this_joint_capsule_saved_all", "cut_muscles_is_fixed_again", "complete_opera_report_is_given", "hr_average_size",
    "hr_average_location", "assesses_x-ray", "x-ray_at_discharge", "two-sided_operation", "foreign_patients",
    "patient-reported_complications"
]

# Fetch the content of the webpage
response = requests.get(url)

# Check for a successful response
if response.status_code == 200:
    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Extract all rows from the table
    rows = table.find_all('tr')

    # Extract the data into a list of dictionaries
    data = []
    for row in rows:
        cols = row.find_all('td')
        row_data = []
        for col in cols:
            # If there is an <a> tag, extract the URL
            link = col.find('a')
            if link:
                url = link.get('href')
                text = link.text
                # Combine text and URL
                row_data.append(f"{text} ({url})")
            else:
                row_data.append(col.text.strip())
        data.append(row_data)

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Remove the first 6 rows and start from the 7th row
    df = df.iloc[6:1042].reset_index(drop=True)

    # Apply the correct column names
    df.columns = correct_column_names

    # Save the DataFrame to a CSV file
    df.to_csv('table_with_correct_columns.csv', index=False)
    print("HTML table with correct column names successfully converted to CSV!")
    df.to_csv('./Find-a-Doctor/data/hip_surgeons.csv', index=False)
    # Read the CSV file to check its head
    df_loaded = pd.read_csv('table_with_correct_columns.csv')

    # Display all column names
    print("Column Names:")
    print(df_loaded.columns.tolist())

    # Set pandas options to display all columns
    pd.set_option('display.max_columns', None)  # Show all columns

    # Display the first few rows with all columns
    print(df_loaded.head())

    # Display DataFrame information
    df_loaded.info()

else:
    print("Failed to retrieve the webpage.")



# In[4]:


df


# In[ ]:




