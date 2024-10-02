#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
data = './Find-a-Doctor/data/hip_surgeons.csv'


# In[2]:


df = pd.read_csv(data, sep=',')


# In[3]:


df


# In[5]:


# pandas settings are local to with statement.
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(df['orthopedic_surgeon_surname'])


# In[3]:


columns = ['orthopedic_surgeon_first_name', 'orthopedic_surgeon_surname', 'jpg_doctor', 'born_year', 'address', 'street', 'local', 'city', 'postal_code', 'country', 'phone_normal', 'phone_free_of_charge', 'fax', 'mobile', 'email', 'homepage', 'number_hr', 'adjusted', 'number_thr', 'number_bmhr', 'type_of_hr_prosthesis', 'type_of_thr_prosthesis', 'operational_technique', 'anesthetic', 'cement_femur_side', 'this_joint_capsule_saved_all', 'cut_muscles_is_fixed_again', 'complete_opera_report_is_given', 'hr_average_size', 'hr_average_location', 'assesses_x-ray', 'x-ray_at_discharge', 'two-sided_operation', 'foreign_patients', 'patient-reported_complications']
values = []
values.append(['Michael', 'Crovetti Jr.', 'NaN', 'NaN', 'Crovetti Orthopaedics and Sports Medicine', '2779 West Horizon Ridge Pkwy', 'Suite #200', 'Henderson', 'NV 89052', 'USA', '(702) 990-2290', 'NaN', 'NaN', 'NaN', 'NaN', 'http://www.crovettiortho.com/Crovetti.html'] + ['NaN']*19)
values.append(['John A.', 'Evans', 'NaN', 'NaN', 'NaN', '414 Navarro Street', 'Suite 1128', 'San Antonio', 'TX 78205', 'USA', '(210) 351-6500', 'NaN', '(210) 351-6509', 'NaN', 'NaN', 'http://orthoevans.com/', '200+'] + ['NaN']*18)
values.append(['M. Christine', 'Young', 'NaN', 'NaN', 'Fracture Clinic', '4040 Finch Avenue East', 'Suite 205', 'Scarborough', 'Ontarion MIS 4V5', '(416) 754-7312' , 'NaN', '(416) 754-0116', '(416) 495-2557', 'mcyoung@bellnet.ca', 'NaN', '200+'] +['NaN']*18)
values.append(['Myung Chul', 'Yoo', 'NaN', 'NaN', 'Dept. of Orthopedic Surgery Kyung Hee University Hospital at Gang-dong', 'Sangil-dong, Gangdong-gu', '#149', 'Seoul 134-727', 'Korea', '+82-2-440-7704, 9', 'NaN', 'NaN', 'NaN', 'mcyookuh@chol.com', 'http://www.kuims.or.kr/index.html', '1000+', 'NaN', 'NaN', 'NaN', 'ConservePlus'] + ['NaN']*14)
values.append(['Andrew', 'Pearson', 'NaN', 'NaN', 'Birmingham Hip Clinic BMI Priory Hospital', 'Priory Road', 'NaN', 'Edgbaston', 'Birmingham B5 7UG', 'United Kingdom', '05600496630', 'NaN', 'NaN', 'NaN', 'info@birmingham-hip-clinic.com', 'http://www.birmingham-hip-clinic.com/', '800+'] + ['NaN']*18)
values.append (['John', 'Skinner', 'NaN', 'NaN', 'Royal National Orthopaedic Hospital', 'Brockley Hill', 'NaN', 'Stanmore' , 'Middlesex HA7 4LP', 'United Kingdom', '020 8954 2300', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', '500+'] + ['NaN']*18)
for val in values: 
    d = dict(zip(columns, val))
    df.loc[len(df)] = d
df = df.replace('NaN', 'missing_value')              


# In[4]:


#print(df[df['orthopedic_surgeon_surname'].str.contains(r'[?]')])
import numpy as np
df = df.drop_duplicates()
#df = df.replace(np.nan, None)

df['orthopedic_surgeon_surname'] = df['orthopedic_surgeon_surname'].str.replace('Mc ', 'Mc')
df['orthopedic_surgeon_first_name'] = df['orthopedic_surgeon_first_name'].str.replace(',', '')

df['orthopedic_surgeon_first_name'] = df['orthopedic_surgeon_first_name'].where(df['orthopedic_surgeon_surname'] != 'Masonis', 'John L.')
df = df.fillna('missing_value')
df.drop(df[df['orthopedic_surgeon_surname'].str.contains(r'[?]')].index, inplace=True)
for index, row in df.iterrows():
    
    print (row['orthopedic_surgeon_surname'])


# In[5]:


df


# In[5]:


df.to_csv(data, index=False)


# In[6]:


df = pd.read_csv(data, sep=',')


# In[8]:


df.head()


# In[8]:


import requests
from bs4 import BeautifulSoup

# URL of the web page to scrape
url = 'https://www.hipresurfacingsite.com/list-of-doctors.php'

# Send a GET request to the web page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <strong> tags on the page
    strong_tags = soup.find_all('strong')
    
    # Extract and store the names of doctors
    doctors = []
    for tag in strong_tags:
        name = tag.get_text(strip=True)
        # Append the name to the list if it seems to be a doctor's name
        # This can be customized if needed (e.g., by checking the length or format)
        if len(name.split()) >= 2:  # Assuming names are at least two words
            doctors.append(name)
    
    # Display the list of doctors
    for doctor in doctors:
        print(doctor)
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")


# In[17]:


with open('names.txt', 'r') as file:
    # Create an empty list to store the lines
    lines = []

    # Iterate over the lines of the file
    for line in file:
        # Remove the newline character at the end of the line
        line = line.strip().split()

        # Append the line to the list
        lines.append(line)
    print(lines)    


# In[10]:


print(df.columns.tolist())


# In[7]:


with open('names.txt', 'r') as file:
    lines = file.readlines()
    for line in lines: line = line.strip().split() 
    n = len(lines)
new_col = []
for index, row in df.iterrows():
    f = row['orthopedic_surgeon_first_name'].strip().split()[0]
    s = row['orthopedic_surgeon_surname'].strip()
   # print(s)
    #print(f)
    #print(row['Orthopedic surgeon first name'], row['Orthopedic surgeon surname'])
    for line in lines:
                
        if s in line:
           # print(s)
            if f in line:        
                new_col.append('Yes')
               # print(f, s, line)
                
                lines.remove(line)
                #lines.remove(r'\n')
                break
           # elif f not in line: print('*', f, s, line)
    if len(new_col) == index: new_col.append('No')
#print(new_col)
print(index, len(new_col))
print(new_col.count('Yes'), n)
print(lines)
#print(new_col)


# In[13]:


df.columns


# In[8]:


df.insert(loc = 34,
          column = 'patient-reported_positive_outcomes',
          value=new_col)


# In[7]:


check = df[(df['patient-reported_positive_outcomes'] == 'No')]
print(check['orthopedic_surgeon_surname'])


# In[10]:


df


# In[9]:


df.to_csv(data, index=False)


# In[1]:


import pandas as pd
data = './Find-a-Doctor/data/hip_surgeons.csv'


# In[2]:


df = pd.read_csv(data, sep=',')


# In[4]:


df = df.drop('id', axis='columns')


# In[5]:


df


# In[6]:


df.to_csv(data, index=False)


# In[12]:


#df1 = df1.drop('id', axis='columns')
df1.insert(loc = 0,
          column = 'id',
          value=[str(i) for i in range(1032)])
df1


# In[14]:


data_index = './Find-a-Doctor/data/hip_surgeons_index.csv'
df.to_csv(data, index=False)


# In[ ]:




