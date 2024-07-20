import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import numpy as np

# install plotly express 

#!pip install plotly
#!unzip all_data_neet_2024.zip
# Load the data
data1 = pd.read_csv('all_data_neet_2024_1.csv')
data2 = pd.read_csv('all_data_neet_2024_2.csv')
data3 = pd.read_csv('all_data_neet_2024_3.csv')
data4 = pd.read_csv('all_data_neet_2024_4.csv')
data = pd.concat([data1, data2, data3, data4])

# Sidebar for filters
st.sidebar.title("Filters")
cutoff_min, cutoff_max = st.sidebar.slider("Cutoff Marks Range:", min_value=int(data['Marks'].min()), max_value=int(data['Marks'].max()), value=(653, int(data['Marks'].max())))
selected_states = st.sidebar.multiselect("Select State:", options=data['State'].unique(), default=data['State'].unique())
selected_districts = st.sidebar.multiselect("Select District:", options=data['District'].unique(), default=data['District'].unique())

# Filter the DataFrame
filtered_data = data[(data['Marks'] >= cutoff_min) & (data['Marks'] <= cutoff_max) & (data['State'].isin(selected_states)) & (data['District'].isin(selected_districts))]

# Main Panel
st.title("NEET 2024 Results Data Analysis")
# add a subheader
st.markdown("### Analysis of NEET 2024 Results Data some basic visualizations")
## add a instruction
st.markdown("#### Instructions:")
st.markdown("1. Use the sidebar to filter the data based on cutoff marks, state, and district.")
st.markdown("2. The main panel will display the visualizations based on the selected filters.")
st.markdown("3. The data table will display the filtered data.")
st.markdown("4. The number of students per center will be displayed in a table.")
st.markdown("5. The normal distribution of marks for the top ten centers will be displayed.")

st.markdown("**Data Source:** [NEET Website](https://neet.ntaonline.in/frontend/web/common-scorecard/index), Scraped and analysis by [@kushalkmrd](https://x.com/kushalkmrd)")

# Plot the number of Candidates per state for top centers
state_counts = filtered_data['State'].value_counts().reset_index()
state_counts.columns = ['State', 'count']
fig_state = px.bar(state_counts, x='State', y='count', labels={'State': 'State', 'count': 'Number of Candidates'}, title='Top Centers per State', template='plotly_dark')
fig_state.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_state, use_container_width=True)

# Plot the number of Candidates per district for top centers
district_counts = filtered_data['District'].value_counts().reset_index()
district_counts.columns = ['District', 'count']
fig_district = px.bar(district_counts, x='District', y='count', labels={'District': 'District', 'count': 'Number of Candidates'}, title='Top Centers per District', template='plotly_dark')
fig_district.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_district, use_container_width=True)

# Plot the number of Candidates per city for top centers
city_counts = filtered_data['City'].value_counts().reset_index()
city_counts.columns = ['City', 'count']
fig_city = px.bar(city_counts, x='City', y='count', labels={'City': 'City', 'count': 'Number of Candidates'}, title='Top Centers per City', template='plotly_dark')
fig_city.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_city, use_container_width=True)

# Plot the distribution of marks for top centers
fig_marks = px.histogram(filtered_data, x='Marks', title='Distribution of Marks for Filtered Range', template='plotly_dark')
fig_marks.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_marks, use_container_width=True)

# Data Table
# add a title to the table
st.markdown("### Full Data Table with the selected range for marks")
st.dataframe(filtered_data)

# Number of Candidates per center table
# add a title to the table
st.markdown("### Number of Students per Center in the selected range")
center_counts = filtered_data['Center No'].value_counts().reset_index()
center_counts.columns = ['Center No', 'Number of Students']
center_counts = center_counts.merge(data[['Center No', 'Center Name']].drop_duplicates(), on='Center No', how='left')
st.dataframe(center_counts)

# Plot the normal distribution of marks for the top ten centers
top_centers = center_counts.nlargest(10, 'Number of Students')

fig = go.Figure()



for center_no in top_centers['Center No']:
    center_data = filtered_data[filtered_data['Center No'] == center_no]['Marks']
    fig.add_trace(go.Histogram(x=center_data, nbinsx=30, name=f'Center No: {center_no}', opacity=0.75))

fig.update_layout(title='Distribution of Marks for Top Ten Centers',
                  xaxis_title='Marks',
                  yaxis_title='Frequency',
                  barmode='overlay',
                  template='plotly_dark')

st.plotly_chart(fig)

# Adding a watermark and disclaimer
st.markdown("""
### Note:
- Data scraped by [Twitter @kushalkmrd](https://x.com/kushalkmrd)
- Email: kushalkmrd@gmail.com
- May not be entirely accurate, use at your own risk. 
- For informational purposes only and no accuracy guaranteed as there can be errors in scraping/processing.
""")

# Run this app with `streamlit run app.py` command in terminal
