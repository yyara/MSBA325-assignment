import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px
import matplotlib.pyplot as plt

# Load data function (same as in your code)
@st.cache_data
def load_data():
    data = pd.read_csv("All Countries.csv")
    return data

# Load data
data = load_data()

# Background Image
background_image = "map.jpg"
st.image(background_image, use_column_width=True)


# Explanation about the Dataset
st.title("About the Dataset")
st.markdown("""
    The chosen dataset contains information about various countries and includes the following columns:

    - **Currency**: Currency used in the country.
    - **Capital City**: Capital city of the country.
    - **GDP**: Gross domestic product of the country.
    - **Continent**: Continent where the country is located.
    - **Latitude**: Geographic latitude coordinate.
    - **Longitude**: Geographic longitude coordinate.
    - **Agricultural Land**: Percentage of land used for agriculture.
    - **Forest Area**: Percentage of land covered by forests.
    - **Land Area**: Total land area of the country.
    - **Population**: Total land area of the country.
    - ... (and more columns with various economic, social, and environmental data)

    I chose a few of these information to display them in the visualizations below.
    """
)


# Introduction and Explanation for Map Visualization
st.title("Suicide Rates by Location Map")
st.markdown("""
    This interactive map visualizes suicide rates across different countries.
    Use the slider to filter by suicide rate range and the search box to find specific countries or regions.
    The markers' colors represent different suicide rate levels.
    """
)

# Slider to Filter Suicide Rate Range
min_rate, max_rate = st.slider("Filter by Suicide Rate Range", 0.0, 50.0, (0.0, 50.0))

# Search Box for Specific Countries or Regions
search_term = st.text_input("Search for a Country or Region")

# Create Folium Map and Add Markers
m = folium.Map(location=[0, 0], zoom_start=2)

for index, row in data.iterrows():
    suicide_rate = row["suicide_rate"]
    lat = row["latitude"]
    lon = row["longitude"]
    country = row["country"]

    # Filter based on the selected rate range
    if min_rate <= suicide_rate <= max_rate:
        # Customize marker color, size, and popup information based on the suicide rate
        if suicide_rate > 15:
            marker_color = "red"
            marker_size = 10
        elif suicide_rate > 10:
            marker_color = "orange"
            marker_size = 8
        else:
            marker_color = "green"
            marker_size = 6

        # Filter based on the search term
        if search_term.lower() in country.lower():
            folium.CircleMarker(
                location=[lat, lon],
                radius=marker_size,
                popup=f"Country: {country}<br>Suicide Rate: {suicide_rate}",
                color=marker_color,
                fill=True,
                fill_color=marker_color,
                fill_opacity=0.7,
            ).add_to(m)

# Legend Explanation
legend_html = """
    <div style="
        position: absolute;
        top: 10px;
        right: -200px;
        z-index: 1000;
        background-color: white;
        padding: 10px;
        border: 1px solid gray;
        border-radius: 5px;
        opacity: 0.9;
    ">
    <h5>Legend</h5>
    <div style="background-color: red; width: 20px; height: 20px; display: inline-block;"></div><span>&nbsp;High Suicide Rate</span><br>
    <div style="background-color: orange; width: 20px; height: 20px; display: inline-block;"></div><span>&nbsp;Moderate Suicide Rate</span><br>
    <div style="background-color: green; width: 20px; height: 20px; display: inline-block;"></div><span>&nbsp;Low Suicide Rate</span><br>
    </div>
"""
st.markdown(legend_html, unsafe_allow_html=True)

# Display the Folium Map
st_folium(m, width=800, height=400)

# Explanation for Gender Composition Visualization
st.title('Gender Composition by Country')
st.markdown("""
    This chart illustrates the gender composition in the selected country.
    Choose a country from the dropdown menu to see the distribution of female and male populations.
    """
)

# Dropdown for Selecting Country
selected_country = st.selectbox('Select a Country:', data['country'].unique())

# Filter the dataset and Create Bar Chart
filtered_data = data[data['country'] == selected_country]
if len(filtered_data) == 0:
    st.warning(f'No data available for {selected_country}')
else:
    total_population = filtered_data['population_female'] + filtered_data['population_male']
    gender_composition = {
        'Gender': ['Female', 'Male'],
        'Population': [filtered_data['population_female'].values[0], filtered_data['population_male'].values[0]]
    }

    gender_df = pd.DataFrame(gender_composition)

    # Create a bar chart to visualize gender composition
    fig = px.bar(
        gender_df,
        x='Gender',
        y='Population',
        labels={'Gender': 'Gender Composition', 'Population': 'Population'},
        title=f'Gender Composition in {selected_country}',
        color='Gender'
    )

    # Display the bar chart
    st.plotly_chart(fig)

# Explanation for Land Use Comparison Visualization
st.title('Land Use Comparison by Country')
st.markdown("""
    This pie chart displays the land use composition in the selected country.
    Select a country from the dropdown menu to see the distribution of agricultural land, forest area, urban land, and rural land.
    """
)

# Dropdown for Selecting Country
selected_country = st.selectbox('Select a Country:', data['country'].unique(), key='country_select')

# Filter the dataset and Create Pie Chart
filtered_data = data[data['country'] == selected_country]
if len(filtered_data) == 0:
    st.warning(f'No data available for {selected_country}')
else:
    land_use_columns = ['agricultural_land', 'forest_area', 'urban_land', 'rural_land']
    land_use_percentages = [filtered_data[use].values[0] for use in land_use_columns]

    # Define custom colors for the pie chart segments
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#c2c2f0']

    # Create a pie chart with custom colors
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        land_use_percentages, labels=None, autopct='%1.1f%%', startangle=140, colors=colors)

    # Create a custom legend using the same colors
    legend_labels = ['Agricultural Land', 'Forest Area', 'Urban Land', 'Rural Land']
    custom_legend = '<br>'.join([f'<font color="{color}">&#9608; {lbl}</font>' for lbl, color in zip(legend_labels, colors)])
    st.markdown(custom_legend, unsafe_allow_html=True)

    ax.set_title(f'Land Use Composition in {selected_country}')

    # Display the pie chart in Streamlit
    st.pyplot(fig)
