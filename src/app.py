import streamlit as st
import pandas as pd
from pypdf import PdfReader
import plotly.express as px
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import urllib.request
import io
import re

# Function to fetch PDF data from a URL
def fetch_incidents(url):
    headers = {'User-Agent': "Mozilla/5.0"}
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read()
    return io.BytesIO(data)

# Function to extract incidents from PDF data
def extract_incidents(incident_data):
    incidents = []
    pdfreader = PdfReader(incident_data)
    
    for page in pdfreader.pages:
        text = page.extract_text(extraction_mode="layout")
        rows = text.split('\n')
        
        for row in rows:
            row = row.strip()
            
            if 'Date / Time' in row or 'Daily Incident' in row or 'NORMAN POLICE DEPARTMENT' in row:
                continue
            
            if len(row) == 0:
                continue
            
            columns = re.split(r'\s{2,}', row)
            
            if len(columns) != 5:
                continue
            
            incidents.append(tuple(columns))
    
    return incidents

# Function to visualize data
def visualize_data(df):
    # Clustering of Records by Location
    st.subheader("Clustering of Incident Locations")
    if not df.empty:
        kmeans = KMeans(n_clusters=3)
        df['location_hash'] = df['incident_location'].apply(lambda x: hash(x) % 1000)
        df['cluster'] = kmeans.fit_predict(df[['location_hash']])
        fig1 = px.scatter(df, x='location_hash', y='incident_time', color='cluster', title="Incident Location Clusters")
        st.plotly_chart(fig1)

    # Bar Graph Comparison
    st.subheader("Incident Nature Frequency")
    nature_counts = df['nature'].value_counts()
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    nature_counts.plot(kind='barh', ax=ax2, title="Frequency of Incident Natures")
    ax2.set_yticklabels(ax2.get_yticklabels(), fontsize=8)
    st.pyplot(fig2)

    # Line Graph of Incidents by Hour
    st.subheader("Number of Incidents by Hour")
    df['incident_time'] = pd.to_datetime(df['incident_time'], errors='coerce')
    df['hour'] = df['incident_time'].dt.hour
    hourly_incidents = df.groupby('hour').size().reset_index(name='count')
    
    fig3 = px.line(hourly_incidents, x='hour', y='count', 
                   labels={'hour': 'Hour of Day', 'count': 'Number of Incidents'}, 
                   title='Incidents by Hour')
    st.plotly_chart(fig3)

# Main function to run the app
def main():
    st.title("Norman Police Incident Data Visualization")

    # Input for URL or file upload
    url = st.text_input("Enter PDF URL:")
    uploaded_file = st.file_uploader("Or upload a PDF file", type="pdf")

    if url or uploaded_file:
        # Fetch and process data
        pdf_data = fetch_incidents(url) if url else uploaded_file

        incidents = extract_incidents(pdf_data)
        
        # Convert to DataFrame for visualization
        df = pd.DataFrame(incidents, columns=['incident_time', 'incident_number', 'incident_location', 'nature', 'incident_ori'])

        # Display raw data
        st.subheader("Incident Data")
        st.write(df)

        # Visualize the data
        visualize_data(df)
    else:
        st.write("Please enter a URL or upload a PDF file.")

if __name__ == "__main__":
    main()