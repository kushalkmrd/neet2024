import streamlit as st
import pandas as pd
import plotly.express as px

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
st.markdown("**Data Source:** [NEET](https://neet.ntaonline.in/frontend/web/common-scorecard/index), [Twitter @kushalkmrd](https://x.com/kushalkmrd), Email: kushalkmrd@gmail.com")

# Plot the number of entries per state for top centers
state_counts = filtered_data['State'].value_counts().reset_index()
state_counts.columns = ['State', 'count']
fig_state = px.bar(state_counts, x='State', y='count', labels={'State': 'State', 'count': 'Number of Entries'}, title='Top Centers per State', template='plotly_dark')
fig_state.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_state, use_container_width=True)

# Plot the number of entries per district for top centers
district_counts = filtered_data['District'].value_counts().reset_index()
district_counts.columns = ['District', 'count']
fig_district = px.bar(district_counts, x='District', y='count', labels={'District': 'District', 'count': 'Number of Entries'}, title='Top Centers per District', template='plotly_dark')
fig_district.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_district, use_container_width=True)

# Plot the number of entries per city for top centers
city_counts = filtered_data['City'].value_counts().reset_index()
city_counts.columns = ['City', 'count']
fig_city = px.bar(city_counts, x='City', y='count', labels={'City': 'City', 'count': 'Number of Entries'}, title='Top Centers per City', template='plotly_dark')
fig_city.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_city, use_container_width=True)

# Plot the distribution of marks for top centers
fig_marks = px.histogram(filtered_data, x='Marks', nbins=20, title='Distribution of Marks for Top Centers', template='plotly_dark')
fig_marks.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_marks, use_container_width=True)

# Plot the number of entries per center for top centers
center_counts = filtered_data.groupby('Center No').size().reset_index(name='count')
center_counts = center_counts.merge(data[['Center No', 'Center Name']].drop_duplicates(), on='Center No', how='left')
fig_center = px.bar(center_counts, x='Center No', y='count', hover_data={'Center Name': True}, labels={'Center No': 'Center No', 'count': 'Number of Entries'}, title='Top Centers per Center', template='plotly_dark')
fig_center.update_traces(hovertemplate='<b>Center No</b>: %{x}<br><b>Count</b>: %{y}<br><b>Center Name</b>: %{customdata[0]}')
fig_center.add_annotation(
    text="Twitter @kushalkmrd",
    xref="paper", yref="paper",
    x=1, y=-0.2, showarrow=False,
    font=dict(size=12, color="gray")
)
st.plotly_chart(fig_center, use_container_width=True)

# Data Table
st.dataframe(filtered_data)

# Adding a watermark and disclaimer
st.markdown("""
### Note:
- Data scraped by [Twitter @kushalkmrd](https://x.com/kushalkmrd)
- Email: kushalkmrd@gmail.com
- This is a hypothetical analysis for demonstration purposes.
""")

# Run this app with `streamlit run app.py` command in terminal
