import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv('yield_df.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

# Calculate yield per country
yield_per_country = df.groupby('Area')['hg/ha_yield'].sum()

# Calculate yield per item
yield_per_item = df.groupby('Item')['hg/ha_yield'].sum()

# Function to create interactive map for selected crop
def create_map_for_crop(crop):
    crop_df = df[df['Item'] == crop]
    
    fig = px.scatter_geo(crop_df, locations='Area', locationmode='country names', 
                         hover_name='Area',color='hg/ha_yield',
                         projection="mercator", size='hg/ha_yield')
    
    fig.update_geos(showcountries=True)
    fig.update_layout(title=f"Crop Distribution: {crop}", 
                      geo=dict(showland=True, landcolor="#B4CADE"),
                      width=1000,  # Adjust width
                      height=1000)  # Adjust height
    
    return fig

def main():
    st.title("AgriSense")
    st.sidebar.markdown('<h1 style="color: #71c33b;">Crop Selection</h1>', unsafe_allow_html=True)

    # Create crop selection dropdown in the sidebar
    selected_crop = st.sidebar.selectbox("Select Crop", df['Item'].unique())

    # Show map for selected crop
    fig = create_map_for_crop(selected_crop)
    st.plotly_chart(fig)
    
    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Country</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Country"):
        st.bar_chart(yield_per_country)

    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Item</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Item"):
        st.bar_chart(yield_per_item)

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Area</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Area"):
        st.bar_chart(df['Area'].value_counts())

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Items</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Items"):
        st.bar_chart(df['Item'].value_counts())

if __name__ == "__main__":
    main()
