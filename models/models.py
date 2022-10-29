import streamlit as st



def get_url(position,location):
    template = 'https://www.reed.co.uk/api/1.0/search?keywords={}&location={}'
    url = template.format(position,location)
    return url



@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')