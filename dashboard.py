import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#page config
st.set_page_config(layout="wide", page_title="Responsible AI Data Visualization Challenge Dashboard")

#title and description
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

st.markdown('<div class="centered-title">Uneven Progress: Responsible AI in the Global Landscape (Theme 3: Open Theme)</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="centered-text">Discover the stark contrasts in how regions adopt and implement responsible AI principles. This visualization uncovers the global divide, spotlighting regions leading the way, those lagging behind, and the critical thematic areas demanding urgent attention to ensure an equitable AI future.</div>',
    unsafe_allow_html=True
)

st.markdown('<hr style="border: 1px solid grey;"/>', unsafe_allow_html=True)

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
    
    #choropleth map
    fig_map = px.choropleth(
        rankings_df,
        locations='ISO3',
        color='Index score',
        hover_name='Country',
        color_continuous_scale='Viridis',
        projection="natural earth"  
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
            projection_scale=1.1  
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)


# 2. AI Governance by Development Status
with col2:
    st.subheader("AI Governance by Development Status")

    filtered_data = rankings_df[rankings_df['Development_Status'].isin(['Developed', 'Developing', 'Underdeveloped'])]

    avg_values = filtered_data.groupby('Development_Status')['Index score'].mean().reset_index()

    #boxplot
    fig_dev = px.box(
        filtered_data,
        x='Development_Status',
        y='Index score',
        color='Development_Status',
    )
    
    for status, avg in zip(avg_values['Development_Status'], avg_values['Index score']):
        fig_dev.add_trace(
            go.Scatter(
                x=[status],
                y=[avg],
                mode='markers+text',
                marker=dict(color='black', size=10), 
                text=[f"Avg: {avg:.2f}"],  
                textposition='top right',
                textfont=dict(color='cyan', size=14)
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
    st.subheader("Average AI Governance Scores by Region")
    
    filtered_rankings_df = rankings_df[rankings_df['GIRAI_region'] != 0]
    regional_avg = filtered_rankings_df.groupby('GIRAI_region')['Index score'].mean()
    regional_std = filtered_rankings_df.groupby('GIRAI_region')['Index score'].std()
    
    region_colors = {
        'Europe': 'mediumseagreen', 
        'North America': 'mediumseagreen',  
        'Asia and Oceania': 'deepskyblue',  
        'Middle East': 'deepskyblue',  
        'South and Central America': 'deepskyblue',  
        'Africa': 'indianred',  
        'Caribbean': 'indianred' 
    }
    
    
    bar_colors = [region_colors.get(region, 'grey') for region in regional_avg.index]
    
    fig_regional = go.Figure()
    fig_regional.add_trace(
        go.Bar(
            x=regional_avg.index,
            y=regional_avg.values,
            #error_y=dict(type='data', array=regional_std.values),
            name='Regional Score',
            marker=dict(color=bar_colors), 
            text=np.round(regional_avg.values, 2), 
            textposition='inside',  
            textfont=dict(color='white')  
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
    
    filtered_data = data_df[data_df['thematic_area'].isin(thematic_areas_to_include)]
    
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
    thematic_by_development = pd.pivot_table(
        development_analysis,
        values='ta_score',
        index='Development_Status',
        columns='thematic_area',
        aggfunc='mean'
    )

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=thematic_by_development.values,
        x=thematic_by_development.columns,
        y=thematic_by_development.index,
        text=np.round(thematic_by_development.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorscale='RdBu',  
        showscale=True,
        hoverongaps=False
    ))

    fig_heatmap.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(
            title='Thematic Areas',
            tickangle=45
        ),    
        height=400
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)




# 4. Key Metrics Comparison

with col4:
    st.subheader("Key Metrics Comparison for Focus Countries")
    
    selected_countries = ['United States of America', 'India', 'Afghanistan']

    categories = ['Index score', 'PILLAR SCORES', 'DIMENSION SCORES']
    category_aliases = ['Index Score', 'Pillar Score', 'Dimension Score']

    country_colors = {
        'United States of America': 'red',
        'India': 'blue',
        'Afghanistan': 'yellow'
    }

    fig_spider = go.Figure()
    
    for country in selected_countries:

        values = rankings_df[rankings_df['Country'] == country][categories].values[0]

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
            yanchor="top",    # anchor point for y
            y=0.1,          # position below the chart
            xanchor="left",   # anchor point for x
            x=1              # keep same horizontal position as original
        ),
        margin=dict(l=0, r=0, t=30, b=0)  # increased bottom margin to accommodate legend
    )      

    # fig_spider.update_layout(
    #     polar=dict(
    #         radialaxis=dict(visible=True, range=[0, 100], gridcolor='grey', showline=False),
    #         angularaxis=dict(
    #             rotation=247,  
    #             direction="clockwise", 
    #         ),
    #         bgcolor='black'
    #     ),
    #     showlegend=True,
    #     margin=dict(l=0, r=0, t=30, b=0)
    # )
    
    # Render the chart
    st.plotly_chart(fig_spider, use_container_width=True)

col1, col2 = st.columns([3, 1]) 

with col1:
    st.markdown("""
    ---
    Data source: [GIRAI 2024 Edition](https://docs.google.com/spreadsheets/d/1548vd6pfzybRL7xXHgdb6VL_NdCXG11sm5WkLzN3dTg/edit?pli=1&gid=1569144951#gid=1569144951)
    """)

with col2:
    st.markdown("""
    ---
    Designed and Developed by:  
    [Satyam Kumar](https://www.linkedin.com/in/satyamkumar09/) | [Priyansha Upadhyay](https://www.linkedin.com/in/priyansha1306/) | [Jaanavi V](https://www.linkedin.com/in/jaanavi-vemana-b21966256/)  
    """)
    st.markdown("""
    Guided by:  
    [Gobi Ramasamy](https://www.linkedin.com/in/gobiramasamy/)
    """)






