import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(layout="wide", page_title="Responsible AI Data Visualization Challenge Dashboard")

# Add title and description
# Add custom CSS for centering
st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 36px; /* Optional: Adjust size for the title */
        color: white; /* Optional: Adjust color for the title */
        font-weight: bold;
        margin-bottom: 10px;
    }
    .centered-text {
        text-align: center;
        font-size: 18px; /* Optional: Adjust size for the description */
        color: white; /* Optional: Adjust color for the description */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add the title and markdown with centering
st.markdown('<div class="centered-title">Responsible AI Data Visualization Challenge Dashboard (Theme 3: Open Theme)</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="centered-text">This dashboard visualizes various aspects of global Responsible AI maturity across different regions and development statuses.</div>',
    unsafe_allow_html=True
)

# st.title("AI Governance Analysis Dashboard")
# st.markdown("""
# This dashboard visualizes various aspects of global AI governance maturity across different regions and development statuses.
# """)

# Load data
@st.cache_data
def load_data():
    rankings_df = pd.read_excel('data/GIRAI_2024_Edition_Data.xlsx', sheet_name='Rankings and Scores')
    data_df = pd.read_excel('data/GIRAI_2024_Edition_Data.xlsx', sheet_name='Data')
    
    # Data preprocessing
    numeric_columns = ['Index score', 'ta_score', 'fr_weighted_score',
                      'ga_weighted_score', 'nsa_weighted_score']
    
    for col in numeric_columns:
        if col in rankings_df.columns:
            rankings_df[col] = pd.to_numeric(rankings_df[col], errors='coerce')
        if col in data_df.columns:
            data_df[col] = pd.to_numeric(data_df[col], errors='coerce')
    
    rankings_df.fillna(0, inplace=True)
    data_df.fillna(0, inplace=True)
    
    # Add development status
    development_status = {
        'Developed': ['Netherlands', 'United States of America', 'Germany', 'United Kingdom', 'Japan',
                     'France', 'Canada', 'Australia', 'Sweden', 'Switzerland'],
        'Developing': ['China', 'India', 'Brazil', 'Mexico', 'Indonesia', 'Turkey',
                      'Thailand', 'Malaysia', 'South Africa'],
        'Underdeveloped': ['Afghanistan', 'Yemen', 'Sudan', 'Ethiopia', 'Mali', 'Niger',
                           'Burkina Faso', 'Uganda', 'Tanzania', 'Madagascar']
    }
    
    rankings_df['Development_Status'] = 'Other'
    for status, countries in development_status.items():
        rankings_df.loc[rankings_df['Country'].isin(countries), 'Development_Status'] = status
    
    return rankings_df, data_df

rankings_df, data_df = load_data()

# Create layout with columns
col1, col2 = st.columns([2, 1])

# 1. Geographic Heat Map

with col1:
    st.subheader("Global AI Governance Maturity")
    
    # Create choropleth map
    fig_map = px.choropleth(
        rankings_df,
        locations='ISO3',
        color='Index score',
        hover_name='Country',
        color_continuous_scale='Viridis',
        projection="natural earth"  # Use natural earth projection for a polished map look
    )
    
    # Update map layout for better aesthetics
    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,  # Hide map frame
            showcoastlines=True,  # Show coastlines
            coastlinecolor="Gray",  # Coastline color
            landcolor="white",  # Land color
            oceancolor="lightblue",  # Ocean color
            showocean=True,  # Show ocean
            projection_scale=1.1  # Slight zoom
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)


# 2. AI Governance by Development Status
with col2:
    st.subheader("AI Governance by Development Status")
    
    # Filter data for selected development statuses
    filtered_data = rankings_df[rankings_df['Development_Status'].isin(['Developed', 'Developing', 'Underdeveloped'])]
    
    # Calculate average values for each development status
    avg_values = filtered_data.groupby('Development_Status')['Index score'].mean().reset_index()

    # Create the boxplot
    fig_dev = px.box(
        filtered_data,
        x='Development_Status',
        y='Index score',
        color='Development_Status',
    )
    
    # Add average values as a scatter trace
    for status, avg in zip(avg_values['Development_Status'], avg_values['Index score']):
        fig_dev.add_trace(
            go.Scatter(
                x=[status],
                y=[avg],
                mode='markers+text',
                marker=dict(color='black', size=10),  # Black marker for the average value
                text=[f"Avg: {avg:.2f}"],  # Show average value as text
                textposition='top right',
                textfont=dict(color='cyan', size=14)
            )
        )
    
    # Update layout for aesthetics
    fig_dev.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis_title="Development Status",
        yaxis_title="Index Score",
    )
    
    # Display the chart
    st.plotly_chart(fig_dev, use_container_width=True)



# Create second row with columns
col3, col4, col5 = st.columns([1, 1, .75])

# 5. Average AI Governance Scores by Region
with col5:
    st.subheader("Average AI Governance Scores by Region")
    
    filtered_rankings_df = rankings_df[rankings_df['GIRAI_region'] != 0]
    regional_avg = filtered_rankings_df.groupby('GIRAI_region')['Index score'].mean()
    regional_std = filtered_rankings_df.groupby('GIRAI_region')['Index score'].std()
    
    # Define the color scheme for each region
    region_colors = {
        'Europe': 'mediumseagreen',  # Aesthetic green shade
        'North America': 'mediumseagreen',  # Aesthetic green shade
        'Asia and Oceania': 'deepskyblue',  # Aesthetic sky blue shade
        'Middle East': 'deepskyblue',  # Aesthetic sky blue shade
        'South and Central America': 'deepskyblue',  # Aesthetic sky blue shade
        'Africa': 'indianred',  # Aesthetic red shade
        'Caribbean': 'indianred'  # Aesthetic red shade
    }
    
    # Map colors based on region
    bar_colors = [region_colors.get(region, 'grey') for region in regional_avg.index]
    
    fig_regional = go.Figure()
    fig_regional.add_trace(
        go.Bar(
            x=regional_avg.index,
            y=regional_avg.values,
            #error_y=dict(type='data', array=regional_std.values),
            name='Regional Score',
            marker=dict(color=bar_colors),  # Set the colors for each bar
            text=np.round(regional_avg.values, 2),  # Text for average score on top of bars
            textposition='inside',  # Position text inside the bars
            textfont=dict(color='white')  # Set text color to Ivory
        )
    )
    
    fig_regional.update_layout(
        xaxis_title="Region",
        yaxis_title="Average Score",
        xaxis_tickangle=45,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)


# 3. Thematic Focus by Development Status

with col3:
    st.subheader("Thematic Area Scores by Development Status")
    
    # Define the thematic areas to be included
    thematic_areas_to_include = [
        "Access to Remedy and Redress",
        "Children's Rights",
        "Data Protection and Privacy",
        "Gender Equality",
        "International Cooperation",
        "Labour Protection and Right to Work",
        "National AI Policy",
        "Public Participation and Awareness",
        "Responsibility and Accountability",
        "Transparency and Explainability"
    ]
    
    # Filter the data to only include the specified thematic areas
    filtered_data = data_df[data_df['thematic_area'].isin(thematic_areas_to_include)]
    
    # Merge with the rankings dataframe to get development status
    development_analysis = filtered_data.merge(
        rankings_df[['Country', 'Development_Status']],
        left_on='country',
        right_on='Country'
    )
    
    # Filter out "Other" from Development_Status
    development_analysis = development_analysis[development_analysis['Development_Status'] != "Other"]
    
    # Reorder the Development_Status to have 'Developed' on top, 'Developing' in the middle, and 'Underdeveloped' at the bottom
    ordered_status = ['Developed', 'Developing', 'Underdeveloped']
    development_analysis['Development_Status'] = pd.Categorical(
        development_analysis['Development_Status'],
        categories=ordered_status,
        ordered=True
    )
    
    # Create pivot table for thematic area scores by development status
    thematic_by_development = pd.pivot_table(
        development_analysis,
        values='ta_score',
        index='Development_Status',
        columns='thematic_area',
        aggfunc='mean'
    )
    
    # Create heatmap using plotly with updated color scale (Red for low score, Blue for high score)
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=thematic_by_development.values,
        x=thematic_by_development.columns,
        y=thematic_by_development.index,
        text=np.round(thematic_by_development.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorscale='RdBu',  # Red for low scores, Blue for high scores
        showscale=True,
        hoverongaps=False
    ))

    fig_heatmap.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis={'tickangle': 45},
        height=400
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)



# 4. Key Metrics Comparison

with col4:
    st.subheader("Key Metrics Comparison")
    
    # Fixed countries list
    selected_countries = ['United States of America', 'India', 'Afghanistan']
    
    # Prepare data for spider plot
    categories = ['Index score', 'PILLAR SCORES', 'DIMENSION SCORES']
    category_aliases = ['Index Score', 'Pillar Score', 'Dimension Score']
    
    # Create color map for countries
    country_colors = {
        'United States of America': 'red',
        'India': 'blue',
        'Afghanistan': 'yellow'
    }
    
    # Create the figure for the spider plot
    fig_spider = go.Figure()
    
    for country in selected_countries:
        # Get the values for the selected country
        values = rankings_df[rankings_df['Country'] == country][categories].values[0]

        # Add the trace for the country with custom color
        fig_spider.add_trace(go.Scatterpolar(
            r=values,
            theta=category_aliases,
            name=country,
            fill='toself',
            line=dict(color=country_colors[country]),
            text=[f"{v:.1f}" for v in values],
            textposition='top center',
            textfont=dict(color='white', size=14),
            mode='lines+markers+text'
        ))
    
    # Update the layout for the spider plot
    fig_spider.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='grey', showline=False),
            angularaxis=dict(
                rotation=247,  # Start angle for the first category (optional adjustment)
                direction="clockwise",  # Rotate clockwise
            ),
            bgcolor='black'
        ),
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Render the chart
    st.plotly_chart(fig_spider, use_container_width=True)


# Add footer with a hyperlink to the data source
# st.markdown("""
# ---
# Data source: [GIRAI 2024 Edition](https://docs.google.com/spreadsheets/d/1548vd6pfzybRL7xXHgdb6VL_NdCXG11sm5WkLzN3dTg/edit?pli=1&gid=1569144951#gid=1569144951)  

# Designed and Developed by:  
# [Satyam Kumar](https://www.linkedin.com/in/satyamkumar09/) | [Priyansha Upadhyay](https://www.linkedin.com/in/priyansha1306/) | [Jaanavi V] (https://www.linkedin.com/in/jaanavi-vemana-b21966256/)  

# Guided by:  
# [Gobi Ramasamy](https://www.linkedin.com/in/gobiramasamy/)
# """)
col1, col2 = st.columns([1, 2])  # Creates two columns, with the second column being wider

with col1:
    st.markdown("""
    ---
    Data source: [GIRAI 2024 Edition](https://docs.google.com/spreadsheets/d/1548vd6pfzybRL7xXHgdb6VL_NdCXG11sm5WkLzN3dTg/edit?pli=1&gid=1569144951#gid=1569144951)
    """)

with col2:
    st.markdown("""
    Designed and Developed by:  
    [Satyam Kumar](https://www.linkedin.com/in/satyamkumar09/) | [Priyansha Upadhyay](https://www.linkedin.com/in/priyansha1306/) | [Jaanavi V](https://www.linkedin.com/in/jaanavi-vemana-b21966256/)  

    Guided by:  
    [Gobi Ramasamy](https://www.linkedin.com/in/gobiramasamy/)
    """)




