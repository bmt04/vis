import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset from the link
url = 'http://linked.aub.edu.lb/pkgcube/data/d6d94131d25e66ceab3db293144d436a.csv'  # Replace with the actual dataset URL
df = pd.read_csv(url)

# Filter dataset for Sidon District and remove rows where 'Percentage of Women' is 0
filtered_df = df[df['refArea'] == 'http://dbpedia.org/resource/Sidon_District']
filtered_df = filtered_df[filtered_df['Percentage of Women'] != 0]

# Sidebar interactivity - Dropdown for town selection
towns = filtered_df['Town'].unique()
selected_town = st.sidebar.selectbox("Select Town", options=towns)

# Sidebar interactivity - Slider to filter percentage of women
min_percentage, max_percentage = int(filtered_df['Percentage of Women'].min()), int(filtered_df['Percentage of Women'].max())
percentage_filter = st.sidebar.slider("Filter by Percentage of Women", min_percentage, max_percentage, (min_percentage, max_percentage))

# Apply filter for town and percentage of women
filtered_df = filtered_df[(filtered_df['Percentage of Women'] >= percentage_filter[0]) & 
                          (filtered_df['Percentage of Women'] <= percentage_filter[1]) &
                          (filtered_df['Town'] == selected_town)]

# Visualization 1 - Pie chart for gender distribution
if not filtered_df.empty:
    fig_pie = px.pie(filtered_df, names=['Percentage of Women', 'Percentage of Men'], 
                     values=[filtered_df['Percentage of Women'].sum(), filtered_df['Percentage of Men'].sum()],
                     title=f"Gender Distribution in {selected_town}")
    st.plotly_chart(fig_pie)
else:
    st.write("No data available for the selected filters.")

# Visualization 2 - Clustered bar chart for percentages of elderly and youth
if not filtered_df.empty:
    # Create a new dataframe with only the columns needed for elderly and youth percentages
    age_df = filtered_df[['Percentage of Eldelry - 65 or more years ', 'Percentage of Youth - 15-24 years']]
    
    # Melt the dataframe to reshape it for plotting
    age_df_melted = age_df.melt(var_name='Age Group', value_name='Percentage')

    # Clustered bar chart
    fig_age = px.bar(age_df_melted, x='Age Group', y='Percentage', 
                     title=f"Elderly and Youth Percentages in {selected_town}",
                     color='Age Group', barmode='group',
                     labels={'Age Group': 'Age Group', 'Percentage': 'Percentage'})
    
    st.plotly_chart(fig_age)
else:
    st.write("No data available for elderly and youth percentages.")
