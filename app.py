import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('all_data_neet_2024.csv')

# Define the cutoff marks
cutoff_marks = 653

# Filter the DataFrame to get entries with marks above the cutoff
top_centers_df = data[data['Marks'] > cutoff_marks]

# Sidebar for inputs
st.sidebar.title("Filters")
cutoff = st.sidebar.slider("Cutoff Marks:", min_value=int(data['Marks'].min()), max_value=int(data['Marks'].max()), value=cutoff_marks)
selected_states = st.sidebar.multiselect("Select State:", options=data['State'].unique(), default=data['State'].unique())
selected_districts = st.sidebar.multiselect("Select District:", options=data['District'].unique(), default=data['District'].unique())

filtered_data = data[(data['Marks'] > cutoff) & (data['State'].isin(selected_states)) & (data['District'].isin(selected_districts))]

# Main Panel
st.title("Top Centers Data Analysis")

# Plot the number of entries per state for top centers
fig_state = px.bar(filtered_data['State'].value_counts().reset_index(), x='index', y='State', labels={'index': 'State', 'State': 'Number of Entries'}, title='Top Centers per State')
st.plotly_chart(fig_state, use_container_width=True)

# Plot the number of entries per district for top centers
fig_district = px.bar(filtered_data['District'].value_counts().reset_index(), x='index', y='District', labels={'index': 'District', 'District': 'Number of Entries'}, title='Top Centers per District')
st.plotly_chart(fig_district, use_container_width=True)

# Plot the number of entries per city for top centers
fig_city = px.bar(filtered_data['City'].value_counts().reset_index(), x='index', y='City', labels={'index': 'City', 'City': 'Number of Entries'}, title='Top Centers per City')
st.plotly_chart(fig_city, use_container_width=True)

# Plot the distribution of marks for top centers
fig_marks = px.histogram(filtered_data, x='Marks', nbins=20, title='Distribution of Marks for Top Centers')
st.plotly_chart(fig_marks, use_container_width=True)

# Plot the number of entries per center for top centers
fig_center = px.bar(filtered_data['Center No'].value_counts().reset_index(), x='index', y='Center No', labels={'index': 'Center No', 'Center No': 'Number of Entries'}, title='Top Centers per Center')
st.plotly_chart(fig_center, use_container_width=True)

# Data Table
st.dataframe(filtered_data)

# Adding a watermark and disclaimer
st.markdown("""
### Note:
- Data scraped by @kushalkmrd
- This is a hypothetical analysis for demonstration purposes.
""")

