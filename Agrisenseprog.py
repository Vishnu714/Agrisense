import subprocess

# Define a function to install dependencies from requirements.txt
def install_requirements():
    try:
        subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

# Call the function to install dependencies
install_requirements()


import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



# Load your dataset
df = pd.read_csv('yield_df.csv')
df.drop('Unnamed: 0', axis=1, inplace=True)

# Calculate yield per country
yield_per_country = df.groupby('Area')['hg/ha_yield'].sum()

# Calculate yield per item
yield_per_item = df.groupby('Item')['hg/ha_yield'].sum()

# Function to display Matplotlib bar plot upon button click
def display_bar_plot(data, ylabel):
    fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size
    ax.barh(data.index, data.values, color='skyblue')
    ax.set_xlabel('Yield')
    ax.set_ylabel(ylabel)
    ax.set_title(f'Yield per {ylabel}')
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    st.pyplot(fig)

# Function to display countplot
def display_countplot(data, ylabel):
    fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size
    ax.barh(data.index, data.values, color='skyblue')
    ax.set_xlabel('Count')
    ax.set_ylabel(ylabel)
    ax.set_title(f'Frequency of {ylabel}')
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    st.pyplot(fig)

# Function to display yield vs item
def display_yield_vs_item(yield_per_item):
    fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the figure size
    ax.barh(yield_per_item.index, yield_per_item.values, color='green')
    ax.set_xlabel('Yield')
    ax.set_ylabel('Item')
    ax.set_title('Yield per Item')
    plt.tight_layout()  # Adjust layout to prevent overlapping labels
    st.pyplot(fig)

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
    # st.markdown('<h1 style="color: #ffd324;">AgriSense</h1>', unsafe_allow_html=True)
    st.title("AgriSense")
    st.sidebar.markdown('<h1 style="color: #71c33b;">Crop Selection</h1>', unsafe_allow_html=True)

    # Create crop selection dropdown in the sidebar
    selected_crop = st.sidebar.selectbox("Select Crop", df['Item'].unique())

    # Show map for selected crop
    fig = create_map_for_crop(selected_crop)
    st.plotly_chart(fig)
    
    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Country</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Country"):
        
        display_bar_plot(yield_per_country, 'Country')
    
    st.sidebar.markdown('<h2 style="color: #71c33b;">Yield per Item</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Yield per Item"):
        display_bar_plot(yield_per_item, 'Item')

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Area</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Area"):
        display_countplot(df['Area'].value_counts(), 'Area')

    st.sidebar.markdown('<h2 style="color: #71c33b;">Frequency of Items</h2>', unsafe_allow_html=True)
    if st.sidebar.button("Show Frequency of Items"):
        display_countplot(df['Item'].value_counts(), 'Item')

if __name__ == "__main__":
    main()


