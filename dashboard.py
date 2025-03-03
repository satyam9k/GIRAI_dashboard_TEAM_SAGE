import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#page config
st.set_page_config(layout="wide", page_title="Responsible AI Data Visualization Challenge Dashboard")
#title

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center;
        font-size: 34px; /* Adjust size for the title */
        color: white; /* Color of the text */
        font-weight: bold;
        margin-bottom: 10px;
        padding: 10px; /* Adds spacing inside the border */
        border: 2px solid grey; /* Thin grey border around the title */
        background: rgba(0, 123, 255, 0.2); /* Translucent blue background */
        border-radius: 10px; /* Rounded corners for the border */
        font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
    }
    .centered-text {
        text-align: center;
        font-size: 18px; /* Adjust size for the description */
        color: white; /* Color of the text */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="centered-title">
        🤖Uneven Progress: Responsible AI in the Global Landscape (Theme 3: Open Theme)🌎
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .times-text {
        font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
        font-size: 18px; /* Adjust the size of the text */
        color: white; /* Color of the text */
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="times-text">Discover the stark contrasts in how regions adopt and implement responsible AI principles. This visualization uncovers the global divide, spotlighting regions leading the way, those lagging behind, and the critical thematic areas demanding urgent attention to ensure an equitable AI future.</div>',
    unsafe_allow_html=True
)


st.markdown('<hr style="border: 1px solid grey;"/>', unsafe_allow_html=True)

#data
@st.cache_data
def load_data():
    rankings_df = pd.read_excel('data/GIRAI_2024_Edition_Data.xlsx', sheet_name='Rankings and Scores')
    data_df = pd.read_excel('data/GIRAI_2024_Edition_Data.xlsx', sheet_name='Data')
    
    #preprocessing
    numeric_columns = ['Index score', 'ta_score', 'fr_weighted_score',
                      'ga_weighted_score', 'nsa_weighted_score']
    
    for col in numeric_columns:
        if col in rankings_df.columns:
            rankings_df[col] = pd.to_numeric(rankings_df[col], errors='coerce')
        if col in data_df.columns:
            data_df[col] = pd.to_numeric(data_df[col], errors='coerce')
    
    rankings_df.fillna(0, inplace=True)
    data_df.fillna(0, inplace=True)
    
    # development status
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

#layout with columns
col1, col2 = st.columns([2, 1])

# 1. Geographic Heat Map
with col1:
    st.markdown(
        """
        <style>
        .times-title {
            text-align: center;
            font-family: 'Times New Roman', Times, serif;
            font-weight: bold;
            font-size: 32px;
            color: white;
        }
        .centered-text {
            text-align: center;
            font-size: 18px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div class="times-title">
            AI Landscape: Measuring Global Preparedness
        </div>
        """,
        unsafe_allow_html=True
    )

    if "highlight_view" not in st.session_state:
        st.session_state.highlight_view = False  

    toggle_view = st.button("Change View📌")
    if toggle_view:
        st.session_state.highlight_view = not st.session_state.highlight_view

    if st.session_state.highlight_view:

        highlight_countries = ['United States of America', 'India', 'Afghanistan']
        rankings_df['Color'] = rankings_df['Country'].apply(
            lambda x: 'Highlighted' if x in highlight_countries else 'Normal'
        )

        color_discrete_map = {
            'Highlighted': 'gold',
            'Normal': 'lightgrey'
        }

        fig_map = px.choropleth(
            rankings_df,
            locations='ISO3',
            color='Color',
            hover_name='Country',
            hover_data={'Index score': True, 'Color': False},
            color_discrete_map=color_discrete_map,
            projection="natural earth"
        )

        fig_map.update_geos(
            center=dict(lat=20, lon=80),
            projection_scale=2.5
        )

        india_value = rankings_df.loc[rankings_df['Country'] == 'India', 'Index score'].values[0]
        usa_value = rankings_df.loc[rankings_df['Country'] == 'United States of America', 'Index score'].values[0]
        afghanistan_value = rankings_df.loc[rankings_df['Country'] == 'Afghanistan', 'Index score'].values[0]

        fig_map.update_layout(
            annotations=[
                dict(
                    x=0.5, 
                    y=0.1,
                    xanchor='center',
                    yanchor='middle',
                    text=(
                        f"<b>Highlighted Countries:</b><br>"
                        f"<b>India's Index Score:</b> {india_value:.2f}<br>"
                        f"<b>USA's Index Score:</b> {usa_value:.2f}<br>"
                        f"<b>Afghanistan's Index Score:</b> {afghanistan_value:.2f}"
                    ),
                    showarrow=False,
                    font=dict(size=14, color="black"),
                    bgcolor="rgba(255, 255, 255, 0.7)", 
                    bordercolor="black",
                    borderwidth=1
                )
            ]
        )

    else:

        fig_map = px.choropleth(
            rankings_df,
            locations='ISO3',
            color='Index score',
            hover_name='Country',
            color_continuous_scale='Viridis',
            projection="natural earth"
        )

        fig_map.update_geos(
            center=dict(lat=10, lon=20),
            projection_scale=1.5
        )

    fig_map.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="Gray",
            landcolor="white",
            oceancolor="lightblue",
            showocean=True,
        ),
        showlegend=False,
    )

    st.plotly_chart(fig_map, use_container_width=True)

# 2. AI Governance by Development Status
with col2:
    st.markdown(
        """
        <style>
        .times-title {
            text-align: center;
            font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
            font-weight: bold; /* Bold text */
            font-size: 32px; /* Adjust font size */
            color: white; /* Text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="times-title">
            AI Governance Across Development Stages
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter data
    filtered_data = rankings_df[rankings_df['Development_Status'].isin(['Developed', 'Developing', 'Underdeveloped'])]

    # Calculate average values
    avg_values = filtered_data.groupby('Development_Status')['Index score'].mean().reset_index()

    # Calculate other statistics for hover
    stats = filtered_data.groupby('Development_Status')['Index score'].agg(['min', 'max', 'median', 'mean']).reset_index()

    # Boxplot
    fig_dev = px.box(
        filtered_data,
        x='Development_Status',
        y='Index score',
        color='Development_Status',
    )

    # Ensure only relevant stats are displayed
    fig_dev.update_traces(
        hoverinfo="skip",  
        hovertemplate=None,  
        selector=dict(type='box')  
    )

    # Add average markers with detailed hover info
    for status, avg in zip(avg_values['Development_Status'], avg_values['Index score']):
    # Get stats for the current development status
        stat_row = stats[stats['Development_Status'] == status]
        min_val, max_val, median_val, mean_val = stat_row[['min', 'max', 'median', 'mean']].values[0]
    
        fig_dev.add_trace(
            go.Scatter(
                x=[status],
                y=[avg],
                mode='markers+text',
                marker=dict(color='black', size=10),
                text=[f"Avg: {avg:.2f}"],
                textposition='top right',
                textfont=dict(color='white', size=14),
                hovertemplate=(
                    'Development Status: %{x}<br>'
                    'Min: %{customdata[0]:.2f}<br>'
                    'Max: %{customdata[1]:.2f}<br>'
                    'Median: %{customdata[2]:.2f}<br>'
                    'Mean: %{customdata[3]:.2f}<br>'
                    'Avg: %{y:.2f}<br>'
                    '<extra></extra>'
                ),
                customdata=[[min_val, max_val, median_val, mean_val]]  
            )
        )
        
    
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
    st.markdown(
        """
        <style>
        .times-title {
            text-align: center;
            font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
            font-weight: bold; /* Bold text */
            font-size: 32px; /* Adjust font size */
            color: white; /* Text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="times-title">
            Region-wise Average Index Score
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    # Filter data
    filtered_rankings_df = rankings_df[rankings_df['GIRAI_region'] != 0]
    regional_avg = filtered_rankings_df.groupby('GIRAI_region')['Index score'].mean()
    regional_std = filtered_rankings_df.groupby('GIRAI_region')['Index score'].std()

    # Define colors for regions
    region_colors = {
        'Europe': 'mediumseagreen', 
        'North America': 'mediumseagreen',
        'Asia and Oceania': 'deepskyblue',
        'Middle East': 'deepskyblue',
        'South and Central America': 'deepskyblue',
        'Africa': 'indianred',
        'Caribbean': 'indianred'
    }

    # Assign bar colors based on region
    bar_colors = [region_colors.get(region, 'grey') for region in regional_avg.index]

   
    # Create bar chart
    fig_regional = go.Figure()
    fig_regional.add_trace(
        go.Bar(
            x=regional_avg.index,
            y=regional_avg.values,
            name='Regional Score',
            marker=dict(color=bar_colors), 
            text=np.round(regional_avg.values, 2),  # Text inside the bars
            textposition='inside',  
            textfont=dict(color='white', size=14),  
            hovertemplate='%{x}: %{y:.2f}<extra></extra>'  # Custom hover template (No extra text)
        )
    )

    # Update layout for bar chart
    
    fig_regional.update_layout(
        xaxis_title="Region",
        yaxis_title="Average Index Score",
        xaxis_tickangle=45,
        margin=dict(l=0, r=0, t=30, b=0)
    )


    # Display the chart
    st.plotly_chart(fig_regional, use_container_width=True)

# 3. Thematic Focus by Development Status
with col3:
    st.markdown(
        """
        <style>
        .times-title {
            text-align: center;
            font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
            font-weight: bold; /* Bold text */
            font-size: 32px; /* Adjust font size */
            color: white; /* Text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="times-title">
            Thematic Area Scores by Development Status
        </div>
        """,
        unsafe_allow_html=True
    )

    # Add vertical spacing above the heatmap to move it down
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

    # Define thematic areas
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

    # Filter the data
    filtered_data = data_df[data_df['thematic_area'].isin(thematic_areas_to_include)]

    # Merge and process the data
    development_analysis = filtered_data.merge(
        rankings_df[['Country', 'Development_Status']],
        left_on='country',
        right_on='Country'
    )

    development_analysis = development_analysis[development_analysis['Development_Status'] != "Other"]
    
    ordered_status = ['Developed', 'Developing', 'Underdeveloped']
    development_analysis['Development_Status'] = pd.Categorical(
        development_analysis['Development_Status'],
        categories=ordered_status,
        ordered=True
    )

    # Pivot table for heatmap
    thematic_by_development = pd.pivot_table(
        development_analysis,
        values='ta_score',
        index='Development_Status',
        columns='thematic_area',
        aggfunc='mean'
    )

    # Create the heatmap
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=thematic_by_development.values,
        x=thematic_by_development.columns,
        y=thematic_by_development.index,
        text=np.round(thematic_by_development.values, 2),
        texttemplate='%{text}',  # This keeps the text labels in the heatmap
        textfont={"size": 10},
        colorscale='RdBu',
        showscale=True,
        hoverongaps=False,
        hovertemplate="Thematic Area: %{x}<br>Development Status: %{y}<br>Score: %{z:.2f}<extra></extra>"  # Removes duplicate z-value
    ))

    # Update heatmap layout
    fig_heatmap.update_layout(
        margin=dict(l=10, r=10, t=30, b=30), 
        xaxis=dict(
            title='Thematic Areas',
            tickangle=45
        ),
        height=500,
    )

    # Display the heatmap
    st.plotly_chart(fig_heatmap, use_container_width=True)

# # 3. Thematic Focus by Development Status
# with col3:
#     st.markdown(
#         """
#         <style>
#         .times-title {
#             text-align: center;
#             font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
#             font-weight: bold; /* Bold text */
#             font-size: 32px; /* Adjust font size */
#             color: white; /* Text color */
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

#     st.markdown(
#         """
#         <div class="times-title">
#             Thematic Area Scores by Development Status
#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     # Add vertical spacing above the heatmap to move it down
#     st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

#     # Define thematic areas
#     thematic_areas_to_include = [
#         "Access to Remedy and Redress",
#         "Children's Rights",
#         "Data Protection and Privacy",
#         "Gender Equality",
#         "International Cooperation",
#         "Labour Protection and Right to Work",
#         "National AI Policy",
#         "Public Participation and Awareness",
#         "Responsibility and Accountability",
#         "Transparency and Explainability"
#     ]

#     # Filter the data
#     filtered_data = data_df[data_df['thematic_area'].isin(thematic_areas_to_include)]

#     # Merge and process the data
#     development_analysis = filtered_data.merge(
#         rankings_df[['Country', 'Development_Status']],
#         left_on='country',
#         right_on='Country'
#     )

#     development_analysis = development_analysis[development_analysis['Development_Status'] != "Other"]
#     ordered_status = ['Developed', 'Developing', 'Underdeveloped']
#     development_analysis['Development_Status'] = pd.Categorical(
#         development_analysis['Development_Status'],
#         categories=ordered_status,
#         ordered=True
#     )

#     # Pivot table for heatmap
#     thematic_by_development = pd.pivot_table(
#         development_analysis,
#         values='ta_score',
#         index='Development_Status',
#         columns='thematic_area',
#         aggfunc='mean'
#     )

#     # Create the heatmap
#     fig_heatmap = go.Figure(data=go.Heatmap(
#         z=thematic_by_development.values,
#         x=thematic_by_development.columns,
#         y=thematic_by_development.index,
#         text=np.round(thematic_by_development.values, 2),
#         texttemplate='%{text}',  # This keeps the text labels in the heatmap
#         textfont={"color": "white","size": 10}, 
#         colorscale='RdBu',
#         showscale=True,
#         hoverongaps=False,
#         hovertemplate="Thematic Area: %{x}<br>Development Status: %{y}<br>Score: %{z:.2f}<extra></extra>"  # This removes the duplicate z-value
#     ))

# # Display the heatmap
#     st.plotly_chart(fig_heatmap, use_container_width=True)


# 4. Key Metrics Comparison

with col4:
    st.markdown(
        """
        <style>
        .times-title {
            text-align: center;
            font-family: 'Times New Roman', Times, serif; /* Apply Times New Roman font */
            font-weight: bold; /* Bold text */
            font-size: 32px; /* Adjust font size */
            color: white; /* Text color */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="times-title">
            Key Metrics Comparison for Focus Countries
        </div>
        """,
        unsafe_allow_html=True
    )

    # Dropdown for selecting regional focus
    focus_options = {
        "Default Focus (USA, India, Afghanistan)": ['United States of America', 'India', 'Afghanistan'],
        "European Focus (Netherlands, Poland, Albania)": ['Netherlands', 'Poland', 'Albania'],
        "Asian Focus (Singapore, China, Myanmar)": ['Singapore', 'China', 'Myanmar'],
        "Americas Focus (USA, Brazil, Haiti)": ['United States of America', 'Brazil', 'Haiti']
    }
    
    selected_focus = st.selectbox(
        "Select Regional Focus",
        options=list(focus_options.keys()),
        index=0  # Default selection
    )
    
    selected_countries = focus_options[selected_focus]

    # Categories for the spider chart
    categories = ['Index score', 'PILLAR SCORES', 'DIMENSION SCORES']
    category_aliases = ['Index Score', 'Pillar Score', 'Dimension Score']

    # Colors for countries (can expand if needed)
    country_colors = {
        'United States of America': 'red',
        'India': 'blue',
        'Afghanistan': 'yellow',
        'Netherlands': 'orange',
        'Poland': 'purple',
        'Albania': 'pink',
        'Singapore': 'cyan',
        'China': 'green',
        'Myanmar': 'magenta',
        'Brazil': 'gold',
        'Haiti': 'brown'
    }

    # Create the spider chart
    fig_spider = go.Figure()

    for country in selected_countries:
        if country in rankings_df['Country'].values:
            values = rankings_df[rankings_df['Country'] == country][categories].values[0]

            fig_spider.add_trace(go.Scatterpolar(
                r=values,
                theta=category_aliases,
                name=country,
                fill='toself',
                line=dict(color=country_colors.get(country, 'grey')),
                mode='lines+markers+text',
                text=[f"{val:.1f}" for val in values],  
                textposition="top center", 
                textfont=dict(color='white', size=12)  
            ))

    
    # Layout adjustments for spider chart
    fig_spider.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='grey', showline=False),
            angularaxis=dict(
                rotation=247,  
                direction="clockwise", 
            ),
            bgcolor='black'
        ),
        showlegend=True,
        legend=dict(
            yanchor="top",  
            y=-0.1,          
            xanchor="left",   
            x=0.8             
        ),
        margin=dict(l=0, r=0, t=30, b=50)  
    )

    # Render the chart
    st.plotly_chart(fig_spider, use_container_width=True)



col1, col2 = st.columns([3, 1]) 

with col1:
    st.markdown("""
    ---
    Data source: [GIRAI 2024 Edition](https://docs.google.com/spreadsheets/d/1548vd6pfzybRL7xXHgdb6VL_NdCXG11sm5WkLzN3dTg/edit?pli=1&gid=1569144951#gid=1569144951)  
    Analysis Report: [Team Sage Analysis Report](https://drive.google.com/file/d/1k-fm_R4GKyYx70wDXDFLtRzEOYk_AOAC/view?usp=sharing)
    """)


with col2:
    st.markdown("""
    ---
    Designed and Developed by:  
    [Satyam Kumar](https://www.linkedin.com/in/satyamkumar09/) | [Priyansha Upadhyay](https://www.linkedin.com/in/priyansha1306/) | [Jaanavi V](https://www.linkedin.com/in/jaanavi-vemana-b21966256/)  
    """)
    st.markdown("""
    Guided by:  
    [Dr.Gobi Ramasamy](https://www.linkedin.com/in/gobiramasamy/)
    """)







