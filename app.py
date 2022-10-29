from cgitb import enable
import streamlit as st
import requests
import json
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from models.models import convert_df, get_url



_AUTH = st.secrets['REED_AUTH_KEY']



#Sidebar navigation
with st.sidebar:
    st.image('assets/reed_logo.png')
    
    location_selected = st.text_input('City')
    job_selected = st.text_input('Job')
    
    salary_selected = st.slider('Show jobs with salary upto',0,150000,75000,500)
    
    
url = get_url(job_selected,location_selected)

response = requests.get(
    url,
    auth=requests.auth.HTTPBasicAuth(_AUTH,""),
    )

jobs = json.loads(response.text)["results"]

df = pd.DataFrame(jobs)
df = df.rename(columns={
    'jobId':'Id',
    'employerId':'Employer Id',
    'employerName':'Employer Name',
    'employerProfileId':'Employer Profile Id',
    'employerProfileName':'Employer Profile Name',
    'jobTitle':'Job Title',
    'locationName': 'Location Name',
    'minimumSalary':'Minimum Salary',
    'maximumSalary': 'Maximum Salary',
    'currency': 'Currency',
    'expirationDate': 'Expiration Date',
    'date': 'Date Posted',
    'jobDescription': 'Job Description',
    'applications': 'Applications',
    'jobUrl': 'Job URL'
    })

df = df[df['Maximum Salary']<=salary_selected]


st.subheader('Available Jobs')

#This is a AgGrid table
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=False, groupable=True)

gd.configure_selection(selection_mode='multiple',use_checkbox=True)
gridoptions = gd.build()
grid_table = AgGrid(df,gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    height=500,
                    allow_unsafe_jscode = True,
                    theme='alpine' #streamlit, alpine, balham, material
                    )

sel_row = grid_table['selected_rows']
st.subheader('Favourite Jobs')

#Only show table when a job has been added to the list
if len(sel_row)<1:
    st.info('No jobs added to favourite list')
else:
    st.dataframe(sel_row)
    
    csv = convert_df(df)
    st.download_button(
        label = 'Download',
        data = csv,
        file_name = 'jobs_list',
        mime = 'csv',
        on_click = st.balloons
    )

















